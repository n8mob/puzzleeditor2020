from django.contrib import admin

# Register your models here.
from puzzles.models import Puzzle, ClueLine, WinMessageLine, LevelNameLine, Level, Category, Menu


@admin.register(ClueLine)
class ClueLineAdmin(admin.ModelAdmin):
    pass


@admin.register(WinMessageLine)
class WinMessageLineAdmin(admin.ModelAdmin):
    pass


class PuzzleInlineClueLine(admin.TabularInline):
    model = ClueLine

    fk_name = 'clue_in'
    verbose_name = 'Clue Line'
    verbose_name_plural = 'Clue Lines'


class PuzzleInlineWinMessageLine(admin.TabularInline):
    model = WinMessageLine
    fk_name = 'win_message_in'
    verbose_name = 'Win Message Line'
    verbose_name_plural = 'Win Message Lines'


@admin.register(Puzzle)
class PuzzleAdmin(admin.ModelAdmin):
    inlines = [PuzzleInlineClueLine, PuzzleInlineWinMessageLine]


class PuzzleInline(admin.TabularInline):
    model = Puzzle
    show_change_link = True
    can_delete = False
    extra = 0

    readonly_fields = ['full_clue', 'init', 'winText', 'type', 'encoding', 'line_length']
    fields = readonly_fields


class LevelNameLineInline(admin.TabularInline):
    model = LevelNameLine
    fk_name = 'level_name_of'
    verbose_name = 'Level Name Line'
    verbose_name_plural = 'Level Name Lines'
    extra = 0


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    readonly_fields = ['levelNumber']
    inlines = [LevelNameLineInline, PuzzleInline]

    fields = ['levelNumber', 'levelVersion', 'category']


class LevelNameLinePresenter(admin.TabularInline):
    model = LevelNameLine
    fk_name = 'level_name_of'
    verbose_name = 'Name Line'
    verbose_name_plural = 'Name Lines'


class LevelNamePresenter(admin.TabularInline):
    model = Level
    show_change_link = True
    can_delete = False
    extra = 0

    readonly_fields = ['levelNumber', '__str__', 'levelVersion']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [LevelNamePresenter]


class CategoryInline(admin.TabularInline):
    model = Category

    readonly_fields = ['name']

    show_change_link = True
    can_delete = False
    extra = 0


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    inlines = [CategoryInline]

