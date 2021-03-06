# Generated by Django 2.2.4 on 2020-09-18 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0071_clima'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planta',
            name='alias',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Alias'),
        ),
        migrations.AlterField(
            model_name='planta',
            name='ciudad',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Ciudad'),
        ),
        migrations.AlterField(
            model_name='planta',
            name='direccion',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Dirección'),
        ),
        migrations.AlterField(
            model_name='planta',
            name='estado',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='planta',
            name='giro',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Giro'),
        ),
        migrations.AlterField(
            model_name='planta',
            name='pais',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='País'),
        ),
        migrations.AlterField(
            model_name='planta',
            name='region',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Región'),
        ),
        migrations.AlterField(
            model_name='planta',
            name='slug',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='planta',
            name='tipo',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Tipo'),
        ),
    ]
