# Generated by Django 2.2.4 on 2020-09-28 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0075_auto_20200921_1506'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planta',
            name='pcapacitacion',
        ),
        migrations.RemoveField(
            model_name='planta',
            name='pcobertura',
        ),
        migrations.AlterField(
            model_name='notificacion',
            name='idproblema',
            field=models.IntegerField(blank=True, null=True, verbose_name='Id_problema'),
        ),
    ]
