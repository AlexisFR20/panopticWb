# Generated by Django 2.2.4 on 2020-08-17 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0054_areapermiso_permisos'),
    ]

    operations = [
        migrations.AddField(
            model_name='areapermiso',
            name='orden',
            field=models.SmallIntegerField(default=0, verbose_name='Orden'),
        ),
    ]
