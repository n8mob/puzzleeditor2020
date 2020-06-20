from rest_framework import serializers

from puzzles.models import Puzzle, ClueLine, WinMessageLine, Level


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
            'puzzles',
        ]
