# Generated by Django 2.2.4 on 2020-09-07 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entorno', '0006_auto_20200225_1553'),
    ]

    operations = [
        migrations.RenameField(
            model_name='incidente',
            old_name='desc',
            new_name='titulo',
        ),
        migrations.AddField(
            model_name='incidente',
            name='descripcion',
            field=models.TextField(blank=True, default='', max_length=100),
        ),
    ]
