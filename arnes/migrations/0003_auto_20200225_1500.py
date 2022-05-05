# Generated by Django 2.2.4 on 2020-02-25 23:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20200225_1456'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('arnes', '0002_auto_20200129_1603'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='papeleta',
            name='user',
        ),
        migrations.AddField(
            model_name='papeleta',
            name='contacto_logistica',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contacto_logistica', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='papeleta',
            name='contacto_operativo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contacto_operativo', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='papeleta',
            name='evidencia',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='papeleta',
            name='user_aguilas',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_aguilas', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Recomendacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('ponderacion', models.FloatField()),
                ('coste', models.BooleanField(default=False)),
                ('fecha_compromiso', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('en_proceso', 'En proceso'), ('vencido', 'Vencido'), ('cumplido', 'Cumplido'), ('cancelado', 'Cancelado')], default='en_proceso', max_length=100)),
                ('area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='arnes.Categoria_Encuesta')),
                ('encuesta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arnes.Encuesta')),
                ('planta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Planta')),
                ('user_aguilas', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_aguilas', to='core.Planta')),
                ('user_responsable', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_responsable', to='core.Planta')),
            ],
        ),
        migrations.CreateModel(
            name='EvidenciaRecomendacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='')),
                ('documento', models.FileField(blank=True, null=True, upload_to='')),
                ('nota', models.TextField()),
                ('recomendacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arnes.Recomendacion')),
            ],
        ),
    ]
