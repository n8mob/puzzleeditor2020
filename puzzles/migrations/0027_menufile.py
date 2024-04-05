# Generated by Django 5.0.4 on 2024-04-04 23:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0026_alter_category_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('menu', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='puzzles.menu')),
            ],
        ),
    ]
