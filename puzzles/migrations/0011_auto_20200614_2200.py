# Generated by Django 3.0.6 on 2020-06-14 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0010_auto_20200614_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='puzzle',
            name='init_text',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='puzzle',
            name='win_text',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]