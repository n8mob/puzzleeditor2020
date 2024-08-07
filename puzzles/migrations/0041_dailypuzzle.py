# Generated by Django 5.0.4 on 2024-08-03 03:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0040_look_up_encoding_by_encoding_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyPuzzle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique_for_date=True)),
                ('puzzle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='puzzles.puzzle')),
            ],
        ),
    ]
