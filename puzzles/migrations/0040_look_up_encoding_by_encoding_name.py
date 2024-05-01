# Generated by Django 5.0.4 on 2024-04-30 05:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0039_puzzle_encoding'),
    ]

    operations = [
      migrations.RunSQL("""
update main.puzzles_puzzle
set encoding_id = enc1.encId
from (select main.puzzles_puzzle.id            as puzId,
             main.puzzles_puzzle.encoding_name as puzEncName,
             main.puzzles_encoding.encoding_id as encName,
             main.puzzles_encoding.id          as encId
      from puzzles_encoding
               join puzzles_puzzle
                    on puzzles_encoding.encoding_id = main.puzzles_puzzle.encoding_name) as enc1
where puzzles_puzzle.encoding_name = enc1.encName;
      """
          )
    ]
