# Generated by Django 2.2.4 on 2020-08-10 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddmanagement', '0013_auto_20200807_1702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimiento',
            name='gls',
            field=models.FloatField(blank=True, null=True, verbose_name='Gls.'),
        ),
        migrations.AlterField(
            model_name='movimiento',
            name='lts',
            field=models.FloatField(blank=True, null=True, verbose_name='Lts.'),
        ),
        migrations.AlterField(
            model_name='movimiento',
            name='peaje',
            field=models.FloatField(blank=True, null=True, verbose_name='Peaje.'),
        ),
    ]
