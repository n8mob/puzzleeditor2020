# Generated by Django 3.0.6 on 2020-07-26 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0015_auto_20200712_0302'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
        migrations.RemoveField(
            model_name='clueline',
            name='length',
        ),
        migrations.RemoveField(
            model_name='levelnameline',
            name='length',
        ),
        migrations.RemoveField(
            model_name='winmessageline',
            name='length',
        ),
    ]
