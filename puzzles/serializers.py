from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from puzzles.models import Puzzle, ClueLine, WinMessageLine, Level, Menu, Category


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

    class Meta:
        model = Puzzle
        fields = [
            'id',
            'puzzleName',
            'type',
            'encoding',
            'init',
            'winText',
            'clue',
            'winMessage',
            'level'
        ]


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


class MenuSerializer(serializers.ModelSerializer):
    # categories = CategorySerializer(many=True)
    categories = SerializerMethodField(method_name='get_categories')

    @staticmethod
    def get_categories(menu):
        return {c.name: CategorySerializer().to_representation(instance=c) for c in menu.categories.all()}

    class Meta:
        model = Menu
        fields = [
            'menuVersion',
            'categories'
        ]
