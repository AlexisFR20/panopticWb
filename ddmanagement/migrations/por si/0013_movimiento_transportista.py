# Generated by Django 2.2.4 on 2020-08-07 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddmanagement', '0012_remove_movimiento_transportista'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimiento',
            name='transportista',
            field=models.TextField(blank=True, max_length=100, null=True, verbose_name='Información de la Carga'),
        ),
    ]
