# Generated by Django 3.1.13 on 2022-01-27 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cporte', '0002_portecarta_pdf'),
    ]

    operations = [
        migrations.CreateModel(
            name='Autotransporte',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipoTransporte', models.CharField(max_length=10)),
                ('placas', models.CharField(max_length=20)),
                ('anio', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='PorteFigura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=10)),
                ('rfc', models.CharField(max_length=13)),
                ('nombre', models.CharField(max_length=30)),
                ('licencia', models.CharField(max_length=30)),
                ('cp', models.CharField(max_length=6)),
                ('estado', models.CharField(max_length=15)),
                ('municipio', models.CharField(max_length=20)),
                ('colonia', models.CharField(max_length=20)),
                ('calle', models.CharField(max_length=20)),
                ('ext', models.CharField(max_length=10)),
                ('int', models.CharField(max_length=10)),
                ('referencia', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Seguro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aseguradora', models.CharField(max_length=20)),
                ('poliza', models.CharField(max_length=20)),
            ],
        ),
    ]
