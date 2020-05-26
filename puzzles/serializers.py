from rest_framework import serializers

from puzzles.models import Line, Puzzle


class LineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Line
        fields = ['text', 'length', 'clue_in']


class PuzzleSerializer(serializers.ModelSerializer):
    clue_lines = serializers.StringRelatedField(many=True)

    class Meta:
        model = Puzzle
        fields = ['id', 'name', 'clue_lines']
