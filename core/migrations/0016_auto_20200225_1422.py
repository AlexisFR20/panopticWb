# Generated by Django 2.2.4 on 2020-02-25 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20200225_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planta',
            name='region',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='Región'),
        ),
    ]
