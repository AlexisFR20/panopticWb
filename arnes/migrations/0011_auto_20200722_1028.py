# Generated by Django 2.2.4 on 2020-07-22 15:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0048_auto_20200722_1028'),
        ('arnes', '0010_auto_20200622_1735'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria_Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Categoría')),
            ],
        ),
        migrations.CreateModel(
            name='Grado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Grado')),
            ],
        ),
        migrations.AddField(
            model_name='recomendacion',
            name='respuesta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='arnes.Respuesta'),
        ),
        migrations.AlterField(
            model_name='categoria_encuesta',
            name='nombre',
            field=models.CharField(max_length=50, verbose_name='Nombre de Categorí\xada Encuesta'),
        ),
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Curso')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arnes.Categoria_Curso')),
                ('grado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arnes.Grado')),
            ],
        ),
        migrations.CreateModel(
            name='Concentracion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_orden', models.CharField(max_length=50, verbose_name='No. Orden')),
                ('calificacion', models.SmallIntegerField(blank=True, null=True, verbose_name='Calificación')),
                ('fecha_aplicacion', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Fecha de Aplicación')),
                ('veces_aplicados', models.SmallIntegerField(blank=True, default=1, null=True, verbose_name='Veces Aplicados')),
                ('tiempo_dedicado', models.SmallIntegerField(blank=True, default=1, null=True, verbose_name='Tiempo Dedicado')),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arnes.Categoria_Curso')),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Cliente')),
                ('curso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arnes.Curso', verbose_name='Curso')),
                ('grado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arnes.Grado')),
                ('puesto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Role', verbose_name='Puesto')),
                ('sitio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Planta')),
                ('user_aguilas', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_concentraciones', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
