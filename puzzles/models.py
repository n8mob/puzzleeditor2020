from django.db import models
from django.db.models import Manager, QuerySet

from django.utils.text import slugify

CHOICE_TYPE_LENGTH = 32

DECODE_TYPE = 'Decode'
ENCODE_TYPE = 'Encode'
CHOCOLATE_TYPE = 'Chocolate'

PUZZLE_TYPE_CHOICES = [
  (DECODE_TYPE, 'Decode'),
  (ENCODE_TYPE, 'Encode'),
  (CHOCOLATE_TYPE, 'Chocolate'),
]

# These values are sent to the game as-is and compared case-sensitively there,
# so they must stay lowercase (unlike the capitalized puzzle types above).
CLOCK_NONE = 'none'
CLOCK_ADVANCE = 'advance'
CLOCK_SCROLL = 'scroll'

CHOCOLATE_CLOCK_CHOICES = [
  (CLOCK_NONE, 'Taste — player-paced, no clock'),
  (CLOCK_ADVANCE, 'Treat — focus auto-advances, timed'),
  (CLOCK_SCROLL, 'Dessert — conveyor carries letters past a judgment line'),
]

FIXED = 'fixed'
VARIABLE = 'variable'
OTHER = 'other'

ENCODING_TYPE_CHOICES = [
  (FIXED, 'Fixed'),
  (VARIABLE, 'Variable'),
  (OTHER, 'Other')
]


def concat_lines(relation: Manager['Line']):
  return ' '.join(line.text for line in relation.all())


class Encoding(models.Model):
  encoding_id = models.SlugField(max_length=250, unique=True)
  encoding_type = models.CharField(max_length=CHOICE_TYPE_LENGTH, choices=ENCODING_TYPE_CHOICES, default=OTHER)
  encoding = models.JSONField(null=True, blank=True)

  def __str__(self):
    return self.encoding_id


class Menu(models.Model):
  encodings = models.ManyToManyField(Encoding)
  name = models.SlugField(max_length=250, null=True, blank=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name


class MenuFile(models.Model):
  menu = models.ForeignKey(Menu, null=True, blank=True, on_delete=models.SET_NULL)
  file = models.FileField()


class Category(models.Model):
  name = models.CharField(max_length=50)
  menu = models.ForeignKey(Menu, null=True, blank=True, on_delete=models.SET_NULL, related_name='categories')
  sort_order = models.PositiveIntegerField(null=True, blank=True)

  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

    if self.menu:
      self.menu.save()

  def __str__(self):
    return self.name

  class Meta:
    verbose_name_plural = 'Categories'
    ordering = ['sort_order']


class Level(models.Model):
  levelNumber = models.AutoField(primary_key=True, verbose_name='Level Number')
  levelVersion = models.PositiveIntegerField(default=1, verbose_name='Level Version')
  category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='levels')
  slug = models.SlugField(max_length=250, unique=True, blank=True)
  sort_order = models.PositiveIntegerField(null=True, blank=True)
  levelName: models.Manager['LevelNameLine']

  def generate_default_slug(self):
    # Use the concatenated name lines or fallback to level number
    base_name = str(self)
    raw_slug = slugify(base_name)
    return raw_slug[:250] if raw_slug else f'level-{self.levelNumber}'

  def save(self, *args, **kwargs):
    # If the object is new and has no PK, save it first to get the PK
    if not self.pk:
      super().save(*args, **kwargs)
    # Now generate the slug if needed
    if self.should_update_slug():
      self.slug = self.generate_default_slug()
      # Save again only if the slug was just set
      super().save(update_fields=['slug'])
    else:
      # If slug already exists, just save as normal
      super().save(*args, **kwargs)

    if self.category:
      self.category.save()

  def should_update_slug(self):
    if not self.slug:
      return True

    return self.levelName.exists() and self.slug == f'level-{self.levelNumber}'


  class Meta:
    ordering = ['category', 'sort_order']

  def __str__(self):
    concat_name = concat_lines(self.levelName)
    return concat_name if concat_name else f'Level {self.levelNumber}'


class Puzzle(models.Model):
  puzzle_number = models.PositiveSmallIntegerField(null=True, blank=True)
  name = models.CharField(max_length=250)
  slug = models.SlugField(max_length=250, unique=True, blank=True)
  line_length = models.PositiveIntegerField(default=24)
  init = models.CharField(max_length=50, default='', blank=True)
  winText = models.CharField(max_length=50, default='', blank=True)
  type = models.CharField(max_length=CHOICE_TYPE_LENGTH, choices=PUZZLE_TYPE_CHOICES, default=DECODE_TYPE)
  clue: models.Manager['ClueLine']
  winMessage: models.Manager['WinMessageLine']

  # Chocolate settings. Deliberately nullable with no defaults here: the game
  # already defaults every one of these, so a blank field means "use the game's
  # default" and the defaults stay defined in exactly one place. Setting them
  # here too would guarantee the two drift apart.
  # Field names are camelCase to match the JSON the game expects (as winText
  # above already does), so the serializer needs no source= mapping.
  clock = models.CharField(
    max_length=CHOICE_TYPE_LENGTH, choices=CHOCOLATE_CLOCK_CHOICES, null=True, blank=True,
    help_text='Chocolate only. Blank uses the game default (Dessert).')
  scrollSpeed = models.FloatField(
    null=True, blank=True, verbose_name='Scroll speed',
    help_text='Dessert only. Belt speed in rows per second. Blank uses the game default (0.20).')
  scrollAccel = models.FloatField(
    null=True, blank=True, verbose_name='Scroll acceleration',
    help_text='Dessert only. Rows per second added every 10 judged letters. '
              'Blank uses the game default (0.04).')
  maxStrikes = models.PositiveSmallIntegerField(
    null=True, blank=True, verbose_name='Max strikes',
    help_text='Dessert only. Missed letters before the run ends. Blank uses the game default (10).')

  encoding = models.ForeignKey(Encoding, null=True, blank=True, on_delete=models.SET_NULL, related_name='puzzles')

  level = models.ForeignKey(
    Level,
    on_delete=models.CASCADE,
    related_name='puzzles',
    null=True,
    blank=True,
    default=None, )

  class Meta:
    ordering = ['level__category', 'level', 'puzzle_number']

  def __repr__(self):
    clue = self.full_clue()
    if len(clue) > 28:
      clue = clue[:25] + '...'
    return f'{clue} {self.type} {self.encoding} ("{self.name}")'

  def __str__(self):
    return self.__repr__()

  def full_clue(self):
    if self.clue:
      return concat_lines(self.clue)
    else:
      return ''

  @property
  def encoding_name(self):
    return self.encoding.encoding_id if self.encoding else 'No encoding selected'

  def save(self, *args, **kwargs):
    if not self.slug and self.name:
      raw_slug = slugify(self.name)
      if not raw_slug:
        raw_slug = f'{self.level.slug}-puzzle-{self.puzzle_number}'

      self.slug = raw_slug[:250]

    super().save(*args, **kwargs)

    if self.level:
      self.level.save()

    daily_puzzle_manger = getattr(self, 'puzzle_on_date', None)
    if daily_puzzle_manger:
      for daily_puzzle in daily_puzzle_manger.all():
        daily_puzzle.save()


class Line(models.Model):
  text = models.CharField(max_length=80)
  sort_order = models.PositiveSmallIntegerField(null=True, blank=True)

  def __str__(self):
    return self.text

  class Meta:
    abstract = True
    ordering = ['sort_order']


class ClueLine(Line):
  clue_in = models.ForeignKey(
    Puzzle,
    on_delete=models.CASCADE,
    related_name='clue',
    null=True,
    default=None
  )

  def save(self, *args, **kwargs):
    if not self.sort_order and self.clue_in:
      self.sort_order = self.clue_in.clue.count()

    super().save(*args, **kwargs)

    if self.clue_in:
      self.clue_in.save()


class WinMessageLine(Line):
  win_message_in = models.ForeignKey(
    Puzzle,
    on_delete=models.CASCADE,
    related_name='winMessage',
    null=True,
    default=None
  )

  def save(self, *args, **kwargs):
    if not self.sort_order and self.win_message_in:
      self.sort_order = self.win_message_in.winMessage.count()

    super().save(*args, **kwargs)

    if self.win_message_in:
      self.win_message_in.save()


class LevelNameLine(Line):
  level_name_of = models.ForeignKey(
    Level,
    on_delete=models.CASCADE,
    related_name='levelName',
    null=True,
    default=None
  )

  def save(self, *args, **kwargs):
    if not self.sort_order and self.level_name_of:
      self.sort_order = self.level_name_of.levelName.count()

    super().save(*args, **kwargs)

    if self.level_name_of:
      self.level_name_of.save()


class DailyPuzzle(models.Model):
  date = models.DateField(null=False, blank=False, unique=True)
  puzzle = models.ForeignKey(Puzzle, on_delete=models.SET_NULL, related_name='puzzle_on_date', null=True, blank=True)
  updated_at = models.DateTimeField(auto_now=True)

  def encoding(self):
    return self.puzzle.encoding

  @property
  def menu_name(self):
    if self.puzzle and self.puzzle.level and self.puzzle.level.category and self.puzzle.level.category.menu:
      return self.puzzle.level.category.menu.name
    return None
