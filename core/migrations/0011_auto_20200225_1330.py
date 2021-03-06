# Generated by Django 2.2.4 on 2020-02-25 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20200217_1529'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='administrador',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='coordinador',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='ejecutivo_cuenta',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='gerente_operativo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='guardia',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='jefe_grupo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='monitorista',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='supervidor_junior',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='supervisor',
            field=models.BooleanField(default=False),
        ),
    ]
