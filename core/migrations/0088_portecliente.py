# Generated by Django 3.1.13 on 2021-12-06 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0087_delete_computadores'),
    ]

    operations = [
        migrations.CreateModel(
            name='PorteCliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('rfc', models.CharField(max_length=100)),
                ('razon_social', models.CharField(max_length=100)),
                ('regimen_fiscal', models.CharField(max_length=10)),
                ('path_key', models.FileField(upload_to='carta_porte/key/')),
                ('path_cer', models.FileField(upload_to='carta_porte/cer/')),
            ],
        ),
    ]
