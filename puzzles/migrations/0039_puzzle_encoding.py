# Generated by Django 5.0.4 on 2024-04-30 05:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0038_remove_puzzle_encoding'),
    ]

    operations = [
        migrations.AddField(
            model_name='puzzle',
            name='encoding',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='puzzles', to='puzzles.encoding'),
        ),
    ]
