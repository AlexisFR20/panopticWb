# Generated by Django 2.2.4 on 2020-02-11 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entorno', '0002_incidente_label'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alarma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, verbose_name='Nombre')),
                ('url', models.TextField(verbose_name='URL Noticia')),
                ('fecha', models.DateField()),
            ],
        ),
        migrations.AlterField(
            model_name='incidente',
            name='tipo',
            field=models.CharField(choices=[('asalto_transeuntes', 'Asalto a transeuntes'), ('asalto_negocio', 'Asalto a negocio'), ('casa_habitacion', 'Casa habitacion'), ('homicidio', 'Homicidio'), ('secuestro', 'Secuestro'), ('carjacking', 'Carjacking'), ('autopartes', 'Autopartes'), ('hotel', 'Hotel'), ('aeropuerto', 'Aeropuerto')], max_length=30, verbose_name='Tipo'),
        ),
    ]
