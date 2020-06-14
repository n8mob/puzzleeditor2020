from django.db import models


class Puzzle(models.Model):
    name = models.CharField(max_length=250)
    line_length = models.PositiveIntegerField(default=13)

    def __repr__(self):
        return f'Puzzle: {self.name}'

    def __str__(self): return self.__repr__()


class Line(models.Model):
    text = models.CharField(max_length=80)
    length = models.IntegerField()

    def __str__(self):
        return self.text[:self.length]

    class Meta:
        abstract = True


class ClueLine(Line):
    clue_in = models.ForeignKey(Puzzle,
                                on_delete=models.CASCADE,
                                related_name='clue_lines',
                                null=True,
                                default=None)


class WinMessageLine(Line):
    win_message_in = models.ForeignKey(Puzzle,
                                       on_delete=models.CASCADE,
                                       related_name='win_message_lines',
                                       null=True,
                                       default=None)
