from rest_framework import serializers

from puzzles.models import Puzzle, ClueLine, WinMessageLine


class ClueLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClueLine
        fields = ['text', 'length', 'clue_in']


class WinMessageLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = WinMessageLine
        fields = ['text', 'length', 'win_message_in']


class PuzzleSerializer(serializers.ModelSerializer):
    clue_lines = serializers.StringRelatedField(many=True)
    win_message_lines = serializers.StringRelatedField(many=True)

    class Meta:
        model = Puzzle
        fields = [
            'id',
            'name',
            'type',
            'encoding',
            'init_text',
            'win_text',
            'clue_lines',
            'win_message_lines'
        ]
