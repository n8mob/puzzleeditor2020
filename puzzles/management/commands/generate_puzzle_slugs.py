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

            # Uncomment if/when you add a real SlugField
            # puzzle.slug = slug
            # puzzle.save()
