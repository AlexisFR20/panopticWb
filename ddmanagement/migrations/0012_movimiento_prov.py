# Generated by Django 2.2.4 on 2020-08-07 18:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ddmanagement', '0011_remove_movimiento_transportista'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimiento',
            name='prov',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ddmanagement.Proveedor'),
        ),
    ]
