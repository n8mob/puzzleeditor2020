# Generated by Django 5.0.4 on 2024-04-30 00:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0036_puzzle_encoding_name'),
    ]

    operations = [
      migrations.RunSQL("""
      update puzzles_puzzle
      set encoding_name = encoding;
      """)
    ]
