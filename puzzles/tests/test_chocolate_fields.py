import json

from django.test import TestCase

from puzzles.models import CHOCOLATE_TYPE, CLOCK_SCROLL, Puzzle
from puzzles.serializers import PuzzleSerializer


class TestChocolateFields(TestCase):
  """
  The game reads these straight off the serialized puzzle, so the field names
  and the exact choice strings are a contract with the React app — not just
  internal naming. See ChocolateMode.tsx in MAGiE.React.
  """

  def test_chocolate_fields_reach_the_serialized_puzzle(self):
    puzzle = Puzzle.objects.create(
      name='Chocolate 1',
      type=CHOCOLATE_TYPE,
      clock=CLOCK_SCROLL,
      scrollSpeed=0.25,
      scrollAccel=0.05,
      maxStrikes=5,
    )

    data = json.loads(json.dumps(PuzzleSerializer(puzzle).data))

    self.assertEqual('Chocolate', data['type'])
    self.assertEqual('scroll', data['clock'])
    self.assertEqual(0.25, data['scrollSpeed'])
    self.assertEqual(0.05, data['scrollAccel'])
    self.assertEqual(5, data['maxStrikes'])

  def test_unset_chocolate_fields_serialize_as_null(self):
    """
    Null means "use the game's own default", which keeps the defaults defined
    in one place. The game applies them with ??, which treats null as unset.
    """
    puzzle = Puzzle.objects.create(name='Plain decode puzzle')

    data = json.loads(json.dumps(PuzzleSerializer(puzzle).data))

    for field in ('clock', 'scrollSpeed', 'scrollAccel', 'maxStrikes'):
      self.assertIsNone(data[field], f'{field} should be null when unset')

  def test_clock_choices_are_the_lowercase_values_the_game_compares(self):
    clocks = [value for value, _label in Puzzle._meta.get_field('clock').choices]

    self.assertEqual(['none', 'advance', 'scroll'], clocks)

  def test_chocolate_is_an_allowed_puzzle_type(self):
    types = [value for value, _label in Puzzle._meta.get_field('type').choices]

    self.assertIn('Chocolate', types)
