# Generated by Django 3.1.8 on 2021-05-28 02:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0019_auto_20200726_2230'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='puzzle',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='menu',
            name='name',
            field=models.SlugField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='puzzle',
            name='level',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='puzzles', to='puzzles.level'),
        ),
    ]