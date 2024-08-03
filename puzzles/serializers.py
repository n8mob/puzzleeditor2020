import logging

from django.db import IntegrityError
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from puzzles.models import DailyPuzzle, Puzzle, ClueLine, WinMessageLine, Level, Menu, Category, LevelNameLine, Encoding

SORT_ORDER = 'sort_order'


class ClueLineSerializer(serializers.ModelSerializer):
  class Meta:
    model = ClueLine
    fields = ['text', 'length', 'clue_in']


class WinMessageLineSerializer(serializers.ModelSerializer):
  class Meta:
    model = WinMessageLine
    fields = ['text', 'length', 'win_message_in']


class PuzzleSerializer(serializers.ModelSerializer):
  clue = serializers.StringRelatedField(many=True)
  winMessage = serializers.StringRelatedField(many=True)
  puzzleName = serializers.CharField(source='name')
  encoding_name = SerializerMethodField(method_name='get_encoding')

  @staticmethod
  def get_encoding(puzzle):
    if not puzzle:
      return ''
    elif not puzzle.encoding:
      return puzzle.encoding_name or "no encoding"

    return puzzle.encoding.encoding_id

  class Meta:
    model = Puzzle
    fields = [
      'id',
      'puzzleName',
      'type',
      'encoding_name',
      'init',
      'winText',
      'clue',
      'winMessage',
      'level'
    ]

  def create(self, validated_data):
    Puzzle.objects.create(**validated_data)


class LevelSerializer(serializers.ModelSerializer):
  levelName = serializers.StringRelatedField(many=True)
  puzzles = PuzzleSerializer(many=True)

  class Meta:
    model = Level
    fields = [
      'levelName',
      'levelNumber',
      'levelVersion',
      'sort_order',
      'puzzles',
    ]

  def create(self, validated_data):
    Level.objects.create(**validated_data)


class CategoryListSerializer(serializers.ListSerializer):
  def update(self, instance, validated_data):
    pass

  def to_representation(self, data):
    super_list = super().to_representation(data)
    return {cat.name: cat.levels for cat in super_list}


class CategorySerializer(serializers.ModelSerializer):
  levels = LevelSerializer(many=True)
  list_serializer = CategoryListSerializer

  class Meta:
    model = Category
    fields = [
      'levels',
      'sort_order',
    ]


class EncodingSerializer(serializers.ModelSerializer):
  type = serializers.CharField(source='encoding_type')

  class Meta:
    model = Encoding
    fields = [
      'type',
      'encoding'
    ]


class MenuSerializer(serializers.ModelSerializer):
  log = logging.getLogger(__name__)
  categories = SerializerMethodField(method_name='get_categories')
  encodings = SerializerMethodField(method_name='get_encodings')

  @staticmethod
  def get_categories(menu):
    return {c.name: CategorySerializer().to_representation(instance=c) for c in menu.categories.all()}

  @staticmethod
  def get_encodings(menu):
    return {e.encoding_id: EncodingSerializer().to_representation(instance=e) for e in menu.encodings.all()}

  class Meta:
    model = Menu
    fields = [
      'name',
      'menuVersion',
      'encodings',
      'categories'
    ]

  def create(self, validated_data):
    categories = validated_data.pop('categories')
    encodings = validated_data.pop('encodings')
    menu = Menu.objects.create(**validated_data)

    for encoding_json in encodings:
      new_encoding = Encoding.objects.create(**encoding_json)
      new_encoding.menus.add(menu)

    for given_category_order, category_name in enumerate(categories):
      category = categories[category_name]
      category['name'] = category_name
      if SORT_ORDER not in category:
        category[SORT_ORDER] = given_category_order

      levels = category.pop('levels')
      category = Category.objects.create(menu=menu, **category)
      for given_level_order, level in enumerate(levels):
        level_puzzles = level.pop('puzzles')
        level_name_lines = level.pop('levelName')
        if SORT_ORDER not in level:
          level[SORT_ORDER] = given_level_order
        new_level = Level.objects.create(category=category, **level)
        for sort_order, level_name_line in enumerate(level_name_lines):
          LevelNameLine.objects.create(level_name_of=new_level, text=level_name_line, sort_order=sort_order)
        for puzzle in level_puzzles:
          clue_lines = puzzle.pop('clue')
          win_message_lines = puzzle.pop('winMessage')

          if 'puzzleName' in puzzle:
            puzzle['name'] = puzzle.pop('puzzleName')

          if 'level' in puzzle:
            del puzzle['level']

          if 'id' in puzzle:
            puzzle['puzzle_number'] = puzzle.pop('id')

          try:
            new_puzzle = Puzzle.objects.create(level=new_level, **puzzle)
          except IntegrityError as in_e:
            self.log.error(f'{in_e} while creating {puzzle}')
            raise

          for sort_order, clue_line in enumerate(clue_lines):
            ClueLine.objects.create(clue_in=new_puzzle, text=clue_line, sort_order=sort_order)

          for sort_order, win_message_line in enumerate(win_message_lines):
            WinMessageLine.objects.create(win_message_in=new_puzzle, text=win_message_line, sort_order=sort_order)


class DailyPuzzleSerializer(serializers.ModelSerializer):
  puzzle = PuzzleSerializer()
  encoding = EncodingSerializer()

  class Meta:
    model = DailyPuzzle
    fields = '__all__'
