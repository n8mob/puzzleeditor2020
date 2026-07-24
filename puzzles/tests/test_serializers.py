import json

from django.test import TestCase

from puzzles.models import ClueLine, Puzzle
from puzzles.serializers import ClueLineSerializer, PuzzleSerializer


class TestSerializers(TestCase):
  def setUp(self):
    self.puzzle1 = Puzzle.objects.create(name='Puzzle 1')
    self.clue_line1 = ClueLine.objects.create(text='Hello')
    self.line_serializer = ClueLineSerializer(self.clue_line1)

  def test_line_serializer_doesnt_barf(self):
    self.assertTrue(self.clue_line1)
    self.assertEqual('Hello', self.clue_line1.text)

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
    before = self.puzzle1.clue.count()
    ClueLine.objects.create(text="new clue line", clue_in=self.puzzle1)
    self.assertEqual(before + 1, self.puzzle1.clue.count())

  def test_get_line_back(self):
    self.puzzle1.clue.add(self.clue_line1)
    actual_line = self.puzzle1.clue.first()
    self.assertTrue(actual_line)
    self.assertEqual(self.clue_line1, actual_line)
    self.assertEqual(self.clue_line1.text, actual_line.text)

  def test_puzzle_round_trip(self):
    self.puzzle1.clue.add(self.clue_line1)
    puzzle_serializer = PuzzleSerializer(self.puzzle1)
    json_string = json.dumps(puzzle_serializer.data)

    self.assertIn('name', json_string)
    self.assertIn('clue', json_string)
    self.assertIn('Hello', json_string)

    reconstituted = json.loads(json_string)
    self.assertIn('clue', reconstituted)
    self.assertIn('puzzleName', reconstituted)
    self.assertEqual(1, len(reconstituted['clue']))

    self.assertEqual('Hello', reconstituted['clue'][0])
