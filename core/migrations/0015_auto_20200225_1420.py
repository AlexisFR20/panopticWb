# Generated by Django 2.2.4 on 2020-02-25 22:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20200225_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planta',
            name='cliente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Cliente'),
        ),
    ]
