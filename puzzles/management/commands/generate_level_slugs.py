from django.core.management.base import BaseCommand
from django.utils.text import slugify

from puzzles.models import Level

MAX_SLUG_LENGTH = 32

class Command(BaseCommand):
    help = "Generate slug suggestions for each Level based on name lines"

    def handle(self, *args, **options):
        for level in Level.objects.all():
            base_name = str(level)  # Uses your __str__ logic
            raw_slug = slugify(base_name)
            trimmed_slug = raw_slug[:MAX_SLUG_LENGTH]

            # Optional disambiguator: keep if you anticipate possible duplicates
            slug = f"{trimmed_slug}-{level.levelNumber}"

            self.stdout.write(
                f"Level {level.levelNumber}: {base_name} →\t{slug}"
            )

            level.slug = slug
            level.save()
