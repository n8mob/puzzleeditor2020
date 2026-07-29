from puzzles.models import Level, Category
from django.test import TestCase

from puzzles.models import ClueLine, Puzzle


class TestsWithDb(TestCase):

    def test_level_slug_autopopulates_from_name(self):
        cat = Category.objects.create(name="TestCat")
        level = Level.objects.create(category=cat)
        # Add a LevelNameLine to provide a name
        level.levelName.create(text="Chapter 3: Meeting Up with Hepi")
        # Save again to trigger slug generation from name
        level.save()
        self.assertTrue(level.slug)
        self.assertIn("chapter-3-meeting-up-with-hepi", level.slug)

    def test_level_slug_fallback_to_level_number(self):
        cat = Category.objects.create(name="TestCat2")
        level = Level.objects.create(category=cat)
        # No LevelNameLine, so fallback should use level number
        level.save()
        self.assertTrue(level.slug)
        self.assertIn(str(level.levelNumber), level.slug)
    def test_line_creates(self):
        actual = ClueLine.objects.create(text='')

        self.assertTrue(actual)

    def test_line_chars(self):
        actual = ClueLine.objects.create(text='Hello')

        self.assertTrue(actual)
        self.assertEqual('Hello', actual.text)

    def test_puzzle_create(self):
        actual = Puzzle.objects.create()

        self.assertTrue(actual)

    def test_create_two_puzzles_with_default_values(self):
      puzzle1 = Puzzle.objects.create()
      puzzle2 = Puzzle.objects.create()

      self.assertTrue(puzzle1)
      self.assertTrue(puzzle2)

      # slug is unique, so a generated fallback is what keeps a second
      # slug-less puzzle from colliding with the first on ''.
      self.assertEqual(f'puzzle-{puzzle1.pk}', puzzle1.slug)
      self.assertNotEqual(puzzle1.slug, puzzle2.slug)

    def test_puzzle_with_lines(self):
        p = Puzzle.objects.create(slug='test-puzzle')

        lines = [
            ClueLine.objects.create(text='Hello,', clue_in=p),
            ClueLine.objects.create(text='World!', clue_in=p),
        ]

        self.assertTrue(p)
        self.assertTrue(p.clue)
        self.assertEqual(2, p.clue.count())
