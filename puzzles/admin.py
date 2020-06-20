from django.contrib import admin

# Register your models here.
from puzzles.models import Puzzle, ClueLine, WinMessageLine, LevelNameLine, Level


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


class LevelInlineLevelNameLine(admin.TabularInline):
    model = LevelNameLine
    fk_name = 'level_name_of'
    verbose_name = 'Name Line'
    verbose_name_plural = 'Name Lines'


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    inlines = [LevelInlineLevelNameLine]
