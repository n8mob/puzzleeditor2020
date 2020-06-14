from django.db import models


class Puzzle(models.Model):
    DECODE_TYPE = 'Decode'
    ENCODE_TYPE = 'Encode'

    PUZZLE_TYPE_CHOICES = [
        (DECODE_TYPE, 'Decode'),
        (ENCODE_TYPE, 'Encode'),
    ]

    SINGLE_BIT_ENCODING = 'SingleBit'
    DOUBLE_BIT_ENCODING = 'DoubleBit'
    ALPHA_LENGTH_A1_ENCODING = 'AlphaLengthA1'
    THREE_BIT_OCTAL_ENCODING = 'ThreeBitOctal'
    FOUR_BIT_HEX_ENCODING = 'FourBitHex'
    FIVE_BIT_A1 = '5bA1'

    ENCODING_TYPE_CHOICES = [
        (SINGLE_BIT_ENCODING, 'Single Bit'),
        (DOUBLE_BIT_ENCODING, 'Double Bit'),
        (ALPHA_LENGTH_A1_ENCODING, 'Alpha-Length A1'),
        (THREE_BIT_OCTAL_ENCODING, 'Three-Bit Octal'),
        (FOUR_BIT_HEX_ENCODING, 'Four-Bit Hex'),
        (FIVE_BIT_A1, 'Five-Bit A1')
    ]

    name = models.CharField(max_length=250)
    line_length = models.PositiveIntegerField(default=13)
    init_text = models.CharField(max_length=50, default='', blank=True)
    win_text = models.CharField(max_length=50, default='', blank=True)
    type = models.CharField(max_length=32, choices=PUZZLE_TYPE_CHOICES)
    encoding = models.CharField(max_length=32, choices=ENCODING_TYPE_CHOICES)

    def __repr__(self):
        return f'{self.type} {self.encoding}: {self.name}'

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
