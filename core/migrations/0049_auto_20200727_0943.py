# Generated by Django 2.2.4 on 2020-07-27 14:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0048_auto_20200722_1028'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estadofuerza',
            name='cliente',
        ),
        migrations.RemoveField(
            model_name='estadofuerza',
            name='planta',
        ),
        migrations.RemoveField(
            model_name='estadofuerza',
            name='sucursal',
        ),
        migrations.DeleteModel(
            name='CoberturaEstimada',
        ),
        migrations.DeleteModel(
            name='EstadoFuerza',
        ),
    ]
