# Generated by Django 3.0.6 on 2020-07-26 22:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('puzzles', '0018_auto_20200726_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='level',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='levels', to='puzzles.Category'),
        ),
        migrations.AlterField(
            model_name='level',
            name='levelNumber',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='Level Number'),
        ),
        migrations.AlterField(
            model_name='level',
            name='levelVersion',
            field=models.PositiveIntegerField(default=1, verbose_name='Level Version'),
        ),
        migrations.AlterField(
            model_name='puzzle',
            name='encoding',
            field=models.CharField(choices=[('SingleBit', 'Single Bit'), ('DoubleBit', 'Double Bit'), ('AlphaLengthA1', 'Alpha-Length A1'), ('ThreeBitOctal', 'Three-Bit Octal'), ('FourBitHex', 'Four-Bit Hex'), ('5bA1', 'Five-Bit A1')], default='AlphaLengthA1', max_length=32),
        ),
        migrations.AlterField(
            model_name='puzzle',
            name='type',
            field=models.CharField(choices=[('Decode', 'Decode'), ('Encode', 'Encode')], default='Decode', max_length=32),
        ),
    ]
