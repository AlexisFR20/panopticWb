# Generated by Django 2.2.4 on 2020-02-17 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20200217_1525'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planta',
            name='pcapacitacion',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='planta',
            name='pcobertura',
            field=models.FloatField(default=0),
        ),
    ]
