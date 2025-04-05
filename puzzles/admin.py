import datetime
import json

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from char_counter.widget import CharCounterTextInput
from puzzles.forms import DailyPuzzleForm
from puzzles.models import Category, ClueLine, DailyPuzzle, Encoding, Level, LevelNameLine, Menu, MenuFile, Puzzle, WinMessageLine
from puzzles.serializers import MenuSerializer


class BaseLineEditor(admin.TabularInline):
  formfield_overrides = {
    models.CharField: {'widget': CharCounterTextInput},
  }

  class Media:
    css = {
      'all': ('css/char_counter.css',)
    }
    js = ('js/char_counter.js',)


class PuzzleInlineClueLine(BaseLineEditor):
  model = ClueLine

  fk_name = 'clue_in'
  verbose_name = 'Clue Line'
  verbose_name_plural = 'Clue Lines'
  extra = 1


class PuzzleInlineWinMessageLine(BaseLineEditor):
  model = WinMessageLine
  fk_name = 'win_message_in'
  verbose_name = 'Win Message Line'
  verbose_name_plural = 'Win Message Lines'
  extra = 1
  ordering = ('sort_order',)


@admin.register(Puzzle)
class PuzzleAdmin(admin.ModelAdmin):
  inlines = [PuzzleInlineClueLine, PuzzleInlineWinMessageLine]

  @staticmethod
  def clue(puzzle):
    return str(puzzle.full_clue()[:25])

  def formfield_for_dbfield(self, db_field, request, **kwargs):
    if db_field.name == 'winText':
      kwargs['strip'] = False
    return super().formfield_for_dbfield(db_field, request, **kwargs)

  def daily_puzzle_link(self, obj):
    daily_puzzle = obj.puzzle_on_date.first()
    if daily_puzzle:
      url = reverse('admin:puzzles_dailypuzzle_change', args=[daily_puzzle.id])
      return format_html(f'<a href="{url}">{daily_puzzle.date}</a>')

  daily_puzzle_link.short_description = 'Puzzle on Date'

  list_display = ['id', 'puzzle_number', 'level', 'name', 'daily_puzzle_link', 'winText', 'clue', 'type', 'encoding']
  list_editable = ['puzzle_number', 'type', 'encoding']
  list_filter = ['level', 'level__category', 'type', 'encoding']
  list_display_links = ['id', 'name', 'clue', 'winText']
  ordering = ('puzzle_number',)


class LevelNameLinePresenter(BaseLineEditor):
  model = LevelNameLine
  fk_name = 'level_name_of'
  verbose_name = 'Name Line'
  verbose_name_plural = 'Name Lines'


class LevelNameLineInline(BaseLineEditor):
  model = LevelNameLine
  fk_name = 'level_name_of'
  verbose_name = 'Level Name Line'
  verbose_name_plural = 'Level Name Lines'
  extra = 0


class PuzzleInline(admin.TabularInline):
  model = Puzzle
  show_change_link = True
  can_delete = False
  extra = 0

  fields = ['puzzle_number', 'level', 'full_clue', 'init', 'winText', 'type', 'encoding', 'line_length']
  readonly_fields = ['full_clue', 'line_length', 'init', 'winText']
  editable_fields = ['puzzle_number', 'type', 'encoding']


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
  readonly_fields = ['levelNumber', 'level_name']
  inlines = [LevelNameLineInline, PuzzleInline]

  @staticmethod
  def level_name(level):
    return str(level)

  list_editable = ['category', 'sort_order']
  list_display = ['levelNumber', 'sort_order', 'levelVersion', 'level_name', 'category']
  list_display_links = ['levelNumber', 'level_name']
  list_filter = ['category', 'category__menu']
  fields = ['levelNumber', 'levelVersion', 'category']


class LevelInline(admin.TabularInline):
  model = Level
  show_change_link = True
  can_delete = False
  extra = 0

  @staticmethod
  def level_name(level):
    return str(level)

  readonly_fields = ['levelNumber', 'level_name', 'levelVersion']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
  inlines = [LevelInline]

  list_display = ['name', 'menu', 'sort_order']
  list_editable = ['menu', 'sort_order']
  list_filter = ['menu']


class CategoryInline(admin.TabularInline):
  model = Category

  readonly_fields = ['name']

  show_change_link = True
  can_delete = False
  extra = 0


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
  inlines = [CategoryInline]


class MenuInline(admin.TabularInline):
  model = Menu.encodings.through
  extra = 0


@admin.register(Encoding)
class EncodingAdmin(admin.ModelAdmin):
  list_display = ['encoding_id', 'encoding_type']
  list_editable = ['encoding_type']
  inlines = [MenuInline]


@admin.register(MenuFile)
class MenuFileUpload(admin.ModelAdmin):
  def save_model(self, request, obj: MenuFile, form, change):
    menu_json = json.load(obj.file.file)
    if 'name' not in menu_json:
      menu_json['name'] = obj.file.name

    menu_name = menu_json['name']

    menus_by_name = Menu.objects.filter(name=menu_name)

    if not menus_by_name.exists():
      MenuSerializer().create(menu_json)
    else:
      # update
      existing_menu = menus_by_name.get()
      print(f'existing: {existing_menu}')
      print(f'TODO: Update with {menu_json}')


class DateRangeFilter(SimpleListFilter):
  title = _('Date range')
  parameter_name = 'date_range'

  def lookups(self, request, model_admin):
    return (
      ('last_month', _('Last month')),
      ('last_week', _('Last week')),
      ('this_week', _('This week')),
      ('this_month', _('This month')),
      ('next_week', _('Next week')),
      ('next_month', _('Next month')),
    )

  def queryset(self, request, queryset):
    today = datetime.date.today()
    if self.value() == 'last_month':
      first_day_last_month = (today.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
      last_day_last_month = today.replace(day=1) - datetime.timedelta(days=1)
      return queryset.filter(date__range=(first_day_last_month, last_day_last_month))
    elif self.value() == 'last_week':
      last_week_start = today - datetime.timedelta(days=today.weekday() + 7)
      last_week_end = last_week_start + datetime.timedelta(days=6)
      return queryset.filter(date__range=(last_week_start, last_week_end))
    elif self.value() == 'this_week':
      first_day_this_week = today - datetime.timedelta(days=today.weekday())
      return queryset.filter(date__range=(first_day_this_week, today))
    elif self.value() == 'this_month':
      first_day_this_month = today.replace(day=1)
      last_day_this_month = (first_day_this_month + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)
      return queryset.filter(date__range=(first_day_this_month, last_day_this_month))
    elif self.value() == 'next_week':
      next_week_start = today + datetime.timedelta(days=(7 - today.weekday()))
      next_week_end = next_week_start + datetime.timedelta(days=6)
      return queryset.filter(date__range=(next_week_start, next_week_end))
    elif self.value() == 'next_month':
      first_day_next_month = (today.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
      last_day_next_month = (first_day_next_month + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)
      return queryset.filter(date__range=(first_day_next_month, last_day_next_month))
    return queryset


@admin.register(DailyPuzzle)
class DailyPuzzleAdmin(admin.ModelAdmin):
  form = DailyPuzzleForm
  list_display = ['date', 'puzzle']
  list_filter = [DateRangeFilter]
  ordering = ['date']

  class Media:
    js = ('js/daily_puzzle_form.js',)

  def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == 'puzzle':
      if request.POST.get('level'):
        level_id = request.POST.get('level')
        kwargs['queryset'] = Puzzle.objects.filter(level_id=level_id)
      else:
        kwargs['queryset'] = Puzzle.objects.none()
    return super().formfield_for_foreignkey(db_field, request, **kwargs)

  def render_change_form(self, request, context, *args, **kwargs):
    if context.get('original') and context['original'].puzzle:
      # Access the puzzle through the original object
      puzzle = context['original'].puzzle
      level = puzzle.level
      category = level.category
      menu = category.menu

      # Set initial values for the form fields
      context['adminform'].form.initial['menu'] = menu.id
      context['adminform'].form.initial['category'] = category.id
      context['adminform'].form.initial['level'] = level.levelNumber
      context['adminform'].form.initial['puzzle'] = puzzle.id

      # Set data attributes for JavaScript
      context['adminform'].form.fields['menu'].widget.attrs['data-initial'] = menu.id
      context['adminform'].form.fields['category'].widget.attrs['data-initial'] = category.id
      context['adminform'].form.fields['level'].widget.attrs['data-initial'] = level.levelNumber
      context['adminform'].form.fields['puzzle'].widget.attrs['data-initial'] = puzzle.id
    return super().render_change_form(request, context, *args, **kwargs)
