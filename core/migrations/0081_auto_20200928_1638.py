# Generated by Django 2.2.4 on 2020-09-28 21:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0080_planta_region'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='planta',
            name='region',
        ),
        migrations.AddField(
            model_name='planta',
            name='regiones',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Region'),
        ),
    ]
