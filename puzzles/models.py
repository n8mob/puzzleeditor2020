from django.db import models

CHOICE_TYPE_LENGTH = 32

DECODE_TYPE = 'Decode'
ENCODE_TYPE = 'Encode'

PUZZLE_TYPE_CHOICES = [
  (DECODE_TYPE, 'Decode'),
  (ENCODE_TYPE, 'Encode')
]

FIXED = 'fixed'
VARIABLE = 'variable'
OTHER = 'other'

ENCODING_TYPE_CHOICES = {
  FIXED: 'Fixed',
  VARIABLE: 'Variable',
  OTHER: 'Other'
}


def concat_lines(relation):
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
  menuVersion = models.PositiveIntegerField(default=1)

  def __str__(self):
    return self.name


class MenuFile(models.Model):
  menu = models.ForeignKey(Menu, null=True, blank=True, on_delete=models.SET_NULL)
  file = models.FileField()


class Category(models.Model):
  name = models.CharField(max_length=50)
  menu = models.ForeignKey(Menu, null=True, blank=True, on_delete=models.SET_NULL, related_name='categories')
  sort_order = models.PositiveIntegerField(null=True, blank=True)

  def __str__(self):
    return self.name

  class Meta:
    verbose_name_plural = 'Categories'
    ordering = ['sort_order']


class Level(models.Model):
  levelNumber = models.AutoField(primary_key=True, verbose_name='Level Number')
  levelVersion = models.PositiveIntegerField(default=1, verbose_name='Level Version')
  category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL, related_name='levels')
  sort_order = models.PositiveIntegerField(null=True, blank=True)

  class Meta:
    ordering = ['sort_order']

  def __str__(self):
    concat_name = concat_lines(self.levelName)
    return concat_name if concat_name else f'Level {self.levelNumber}'


class Puzzle(models.Model):
  puzzle_number = models.PositiveSmallIntegerField(null=True, blank=True)
  name = models.CharField(max_length=250)
  line_length = models.PositiveIntegerField(default=20)
  init = models.CharField(max_length=50, default='', blank=True)
  winText = models.CharField(max_length=50, default='', blank=True)
  type = models.CharField(max_length=CHOICE_TYPE_LENGTH, choices=PUZZLE_TYPE_CHOICES, default=DECODE_TYPE)

  encoding = models.ForeignKey(Encoding, null=True, blank=True, on_delete=models.SET_NULL, related_name='puzzles')

  level = models.ForeignKey(
    Level,
    on_delete=models.CASCADE,
    related_name='puzzles',
    null=True,
    blank=True,
    default=None, )

  class Meta:
    ordering = ['puzzle_number']

  def __repr__(self):
    clue = self.full_clue()
    if len(clue) > 28:
      clue = clue[:25] + '...'
    return f'{clue} {self.type} {self.encoding} ("{self.name}")'

  def __str__(self): return self.__repr__()

  def full_clue(self):
    return concat_lines(self.clue)

  @property
  def encoding_name(self):
    return self.encoding.encoding_id if self.encoding else 'No encoding selected'


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
    if not self.sort_order:
      self.sort_order = self.clue_in.clue.count()

    self.text = self.text.upper()
    super().save(*args, **kwargs)


class WinMessageLine(Line):
  win_message_in = models.ForeignKey(
    Puzzle,
    on_delete=models.CASCADE,
    related_name='winMessage',
    null=True,
    default=None
    )


class LevelNameLine(Line):
  level_name_of = models.ForeignKey(
    Level,
    on_delete=models.CASCADE,
    related_name='levelName',
    null=True,
    default=None
    )


class DailyPuzzle(models.Model):
  date = models.DateField(null=False, blank=False, unique=True)
  puzzle = models.ForeignKey(Puzzle, on_delete=models.SET_NULL, related_name='puzzle_on_date', null=True, blank=True)

  def encoding(self):
    return self.puzzle.encoding

