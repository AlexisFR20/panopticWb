# Generated by Django 2.2.4 on 2020-02-14 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entorno', '0004_auto_20200213_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidente',
            name='nivel',
            field=models.IntegerField(default=1),
        ),
    ]
