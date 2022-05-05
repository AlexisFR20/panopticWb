# Generated by Django 2.2.4 on 2020-02-25 22:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20200225_1422'),
    ]

    operations = [
        migrations.CreateModel(
            name='Puesto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(default='', max_length=128, verbose_name='Nombre del Puesto')),
            ],
        ),
        migrations.AlterField(
            model_name='sucursal',
            name='region',
            field=models.IntegerField(default=1, verbose_name='Región'),
        ),
        migrations.CreateModel(
            name='EstadoFuerza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.IntegerField(default=1, verbose_name='Región')),
                ('fecha', models.DateField(verbose_name='Fecha')),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Cliente')),
                ('planta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Planta')),
                ('sucursal', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Sucursal')),
            ],
        ),
        migrations.CreateModel(
            name='CoberturaEstimada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cobertura_dia', models.IntegerField(default=0, verbose_name='Cobertura de Día')),
                ('cobertura_noche', models.IntegerField(default=0, verbose_name='Cobertura de Noche')),
                ('estadofuerza', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.EstadoFuerza')),
                ('puesto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Puesto')),
            ],
        ),
    ]
