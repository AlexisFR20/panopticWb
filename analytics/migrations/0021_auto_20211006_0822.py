# Generated by Django 3.1.13 on 2021-10-06 14:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0020_auto_20211005_1039'),
    ]

    operations = [
        migrations.RenameField(
            model_name='f_previsitantes',
            old_name='fecha_agenda',
            new_name='fecha_agendada',
        ),
        migrations.AlterField(
            model_name='f_previsitantes',
            name='fecha_registro',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
