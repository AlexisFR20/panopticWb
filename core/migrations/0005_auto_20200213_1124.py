# Generated by Django 2.2.4 on 2020-02-13 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20200130_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='planta',
            name='region',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
        migrations.AlterField(
            model_name='planta',
            name='nombre',
            field=models.CharField(default='Nombre de planta', max_length=128),
        ),
    ]
