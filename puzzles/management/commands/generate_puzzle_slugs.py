from django.core.management.base import BaseCommand
from django.utils.text import slugify

from puzzles.models import Puzzle

MAX_SLUG_LENGTH = 40


class Command(BaseCommand):
  help = "Generate slug suggestions for each Puzzle based on its name field"

  def handle(self, *args, **options):
    for puzzle in Puzzle.objects.all():
      raw_slug = slugify(puzzle.name)
      trimmed_slug = raw_slug[:MAX_SLUG_LENGTH]

      # Use puzzle_number if available, fallback to ID
      disambiguator = puzzle.puzzle_number if puzzle.puzzle_number else puzzle.id
      slug = f"{trimmed_slug}-{disambiguator}"

      self.stdout.write(
        f"Puzzle {puzzle.id}: {puzzle.name} → {slug}"
      )

      puzzle.slug = slug
      puzzle.save()

  def old_auto_slug_for_safe_keeping(self, *args, **options):
    for puzzle in Puzzle.objects.all():
      if not puzzle.slug and puzzle.name:
        raw_slug = slugify(puzzle.name)
        if not raw_slug:
          raw_slug = f'{puzzle.level.slug}-puzzle-{puzzle.puzzle_number}'

        self.stdout.write(
          f"Puzzle {puzzle.id}: {puzzle.name} → {puzzle.slug}"
        )

        puzzle.slug = raw_slug[:250]
        # could error if not unique
        # would it error on `self.slug = ...` assignment, or here on `.save()`?
        # doesn't really matter if slug is required (which I think it is)
        # if slug is required and not present, we'll get an error.
        # here we're just trying to back-fill the slug from the name.
        puzzle.save()
