from django.test import TestCase

from puzzles.models import ClueLine, Puzzle


class TestsWithDb(TestCase):
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
