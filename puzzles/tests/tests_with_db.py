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

    def test_puzzle_with_lines(self):
        p = Puzzle.objects.create(name='Test Puzzle')

        lines = [
            ClueLine.objects.create(text='Hello,', clue_in=p),
            ClueLine.objects.create(text='World!', clue_in=p),
        ]

        self.assertTrue(p)
        self.assertTrue(p.clue)
        self.assertEqual(2, p.clue.count())
