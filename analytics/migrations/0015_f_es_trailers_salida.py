# Generated by Django 3.1.13 on 2021-09-22 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0014_auto_20210922_0922'),
    ]

    operations = [
        migrations.AddField(
            model_name='f_es_trailers',
            name='salida',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
