# Generated by Django 2.2.4 on 2020-08-12 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ddmanagement', '0014_auto_20200810_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimiento',
            name='emp_transp',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='ddmanagement.Proveedor'),
        ),
    ]
