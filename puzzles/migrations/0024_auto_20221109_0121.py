# Generated by Django 3.2.15 on 2022-11-09 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0023_auto_20221108_2216'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='level',
            options={'ordering': ['sort_order']},
        ),
        migrations.AddField(
            model_name='level',
            name='sort_order',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
