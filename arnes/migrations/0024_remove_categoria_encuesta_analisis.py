# Generated by Django 3.1.13 on 2022-02-04 21:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('arnes', '0023_categoria_encuesta_analisis'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoria_encuesta',
            name='analisis',
        ),
    ]
