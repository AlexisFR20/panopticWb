# Generated by Django 2.2.4 on 2020-08-18 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ddmanagement', '0021_movimiento_tiempo_estimado_google'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimiento',
            name='tiempo_estimado_google',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Tiempo estimado google'),
        ),
    ]
