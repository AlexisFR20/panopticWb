# Generated by Django 2.2.4 on 2020-03-12 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20200311_1639'),
    ]

    operations = [
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre del Rol / Cargo')),
                ('alias_rol', models.CharField(max_length=100, verbose_name='Alias: ')),
            ],
        ),
    ]
