import json

from django.test import TestCase

from puzzles.models import ClueLine, Puzzle
from puzzles.serializers import ClueLineSerializer, PuzzleSerializer


class TestSerializers(TestCase):
    def setUp(self):
        self.line = ClueLine.objects.create(text='Hello')
        self.line_serializer = ClueLineSerializer(self.line)
        self.puzzle = Puzzle.objects.create(name='Puzzle 1')

    def test_line_serializer_doesnt_barf(self):
        self.assertTrue(self.line)
        self.assertEqual('Hello', self.line.text)

        self.assertTrue(self.line_serializer)
        self.assertTrue(self.line_serializer.data)
        self.assertIn('text', self.line_serializer.data)
        self.assertIn('clue_in', self.line_serializer.data)

        self.assertEqual('Hello', self.line_serializer.data['text'])
        self.assertFalse(self.line_serializer.data['clue_in'])

        json_string = json.dumps(self.line_serializer.data)

        self.assertTrue(json_string)
        self.assertIn('text', json_string)
        self.assertIn('clue_in', json_string)

        json_data = json.loads(json_string)

        self.assertIn('text', json_data)
        self.assertIn('clue_in', json_data)
        self.assertFalse(json_data['clue_in'])

        self.assertTrue('Hello', json_data['text'])

    def test_add_one_line_to_puzzle(self):
        self.assertEqual(0, self.puzzle.clue.count())
        self.puzzle.clue.add(self.line)
        self.assertEqual(1, self.puzzle.clue.count())

    def test_get_line_back(self):
        self.puzzle.clue.add(self.line)
        actual_line = self.puzzle.clue.first()
        self.assertTrue(actual_line)
        self.assertEqual(self.line, actual_line)
        self.assertEqual(self.line.text, actual_line.text)

    def test_puzzle_round_trip(self):
        self.puzzle.clue.add(self.line)
        puzzle_serializer = PuzzleSerializer(self.puzzle)
        json_string = json.dumps(puzzle_serializer.data)

        self.assertIn('name', json_string)
        self.assertIn('clue', json_string)
        self.assertIn('Hello', json_string)

        reconstituted = json.loads(json_string)
        self.assertIn('clue', reconstituted)
        self.assertIn('puzzleName', reconstituted)
        self.assertEqual(1, len(reconstituted['clue']))

        self.assertEqual('Hello', reconstituted['clue'][0])
