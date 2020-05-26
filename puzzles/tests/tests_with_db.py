from django.test import TestCase

from puzzles.models import Line, Puzzle


class TestsWithDb(TestCase):
    def setUp(self):
        self.length = 13

    def test_line_creates(self):
        actual = Line.objects.create(length=0)

        self.assertTrue(actual)

    def test_line_chars(self):
        actual = Line.objects.create(text='Hello', length=13)

        self.assertTrue(actual)
        self.assertEqual('Hello', actual.text)
        self.assertEqual(13, actual.length)

    def test_puzzle_create(self):
        actual = Puzzle.objects.create()

        self.assertTrue(actual)

    def test_puzzle_with_lines(self):
        p = Puzzle.objects.create(name='Test Puzzle')

        lines = [
            Line.objects.create(text='Hello,', length=self.length, clue_in=p),
            Line.objects.create(text='World!', length=self.length, clue_in=p),
        ]

        self.assertTrue(p)
        self.assertTrue(p.clue_lines)
        self.assertEqual(2, p.clue_lines.count())
