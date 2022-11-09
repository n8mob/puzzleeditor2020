from django.contrib import admin
from django.db import models

# Register your models here.
from puzzles.models import Puzzle, ClueLine, WinMessageLine, LevelNameLine, Level, Category, Menu
from char_counter.widget import CharCounterTextInput


class BaseLineEditor(admin.TabularInline):
    formfield_overrides = {
        models.CharField: {'widget': CharCounterTextInput},
    }

    class Media:
        css = {
            'all': ('css/char_counter.css', )
        }
        js = ('js/char_counter.js', )


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

    list_display = ['puzzle_number', 'level', 'name', 'clue', 'winText', 'type', 'encoding']
    list_editable = ['puzzle_number']
    list_display_links = ['name']
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

    readonly_fields = ['puzzle_number', 'level', 'full_clue', 'init', 'winText', 'type', 'encoding', 'line_length']
    fields = readonly_fields


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    readonly_fields = ['levelNumber', 'level_name']
    inlines = [LevelNameLineInline, PuzzleInline]

    @staticmethod
    def level_name(level):
        return str(level)

    list_editable = ['category', 'sort_order']
    list_display = ['levelNumber', 'sort_order', 'level_name', 'levelVersion', 'category']
    list_display_links = ['levelNumber', 'level_name']
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


class CategoryInline(admin.TabularInline):
    model = Category

    readonly_fields = ['name']

    show_change_link = True
    can_delete = False
    extra = 0


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = [CategoryInline]
