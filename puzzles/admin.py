from django.contrib import admin

# Register your models here.
from puzzles.models import Puzzle, Line


@admin.register(Line)
class LineAdmin(admin.ModelAdmin):
    pass


class PuzzleInlineLine(admin.TabularInline):
    model = Line


@admin.register(Puzzle)
class PuzzleAdmin(admin.ModelAdmin):
    inlines = [PuzzleInlineLine]
