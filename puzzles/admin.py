import json

from django.contrib import admin
from django.db import models
from django.urls import reverse
from django.utils.html import format_html

from char_counter.widget import CharCounterTextInput
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


@admin.register(DailyPuzzle)
class DailyPuzzleAdmin(admin.ModelAdmin):
  list_display = ['date', 'puzzle']
  list_editable = ['puzzle']
  ordering = ['date']

  def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == 'puzzle':
      daily_puzzles_menu = Menu.objects.filter(name='DailyPuzzles').first()
      menu_id = daily_puzzles_menu.id
      kwargs['queryset'] = Puzzle.objects.filter(level__category__menu_id=menu_id)
    return super().formfield_for_foreignkey(db_field, request, **kwargs)
