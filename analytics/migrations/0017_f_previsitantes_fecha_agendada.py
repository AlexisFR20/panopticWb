# Generated by Django 3.1.13 on 2021-09-23 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0016_auto_20210922_1002'),
    ]

    operations = [
        migrations.AddField(
            model_name='f_previsitantes',
            name='fecha_agendada',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
