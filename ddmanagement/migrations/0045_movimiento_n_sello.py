# Generated by Django 2.2.4 on 2020-10-22 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddmanagement', '0044_auto_20201014_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimiento',
            name='n_sello',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Sello'),
        ),
    ]
