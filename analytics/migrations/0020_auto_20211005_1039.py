# Generated by Django 3.1.13 on 2021-10-05 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0019_f_previsitantes_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='f_previsitantes',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
