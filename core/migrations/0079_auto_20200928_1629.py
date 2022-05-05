# Generated by Django 2.2.4 on 2020-09-28 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0078_auto_20200928_1305'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planta',
            name='region',
        ),
        migrations.AlterField(
            model_name='planta',
            name='estatus_ausentismo_estable',
            field=models.IntegerField(default=0, verbose_name='Estatus Estable de Ausentismo'),
        ),
        migrations.AlterField(
            model_name='planta',
            name='estatus_ausentismo_relevante',
            field=models.IntegerField(default=0, verbose_name='Estatus Relevante de Ausentismo'),
        ),
        migrations.AlterField(
            model_name='planta',
            name='estatus_cobertura_estable',
            field=models.IntegerField(default=0, verbose_name='Estatus Estable de Cobertura'),
        ),
        migrations.AlterField(
            model_name='planta',
            name='estatus_cobertura_relevante',
            field=models.IntegerField(default=0, verbose_name='Estatus Relevante de Cobertura'),
        ),
        migrations.AlterField(
            model_name='planta',
            name='estatus_rotacion_estable',
            field=models.IntegerField(default=0, verbose_name='Estatus Estable de Rotación'),
        ),
        migrations.AlterField(
            model_name='planta',
            name='estatus_rotacion_relevante',
            field=models.IntegerField(default=0, verbose_name='Estatus Relevante de Rotación'),
        ),
        migrations.AlterField(
            model_name='planta',
            name='status',
            field=models.CharField(blank=True, choices=[('optimo', 'Óptimo'), ('estable', 'Estable'), ('relevante', 'Relevante')], default='optimo', max_length=50, null=True),
        ),
    ]
