# Generated by Django 3.1.13 on 2021-09-22 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0011_auto_20210922_0855'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='f_es_trailers',
            name='autoriza',
        ),
        migrations.RemoveField(
            model_name='f_es_trailers',
            name='bill_caja',
        ),
        migrations.RemoveField(
            model_name='f_es_trailers',
            name='caja',
        ),
        migrations.RemoveField(
            model_name='f_es_trailers',
            name='cajon_id',
        ),
        migrations.RemoveField(
            model_name='f_es_trailers',
            name='contenido_caja',
        ),
        migrations.RemoveField(
            model_name='f_es_trailers',
            name='destino',
        ),
        migrations.RemoveField(
            model_name='f_es_trailers',
            name='factura_caja',
        ),
        migrations.RemoveField(
            model_name='f_es_trailers',
            name='factura_remision_ip',
        ),
        migrations.RemoveField(
            model_name='f_es_trailers',
            name='firma_chofer',
        ),
        migrations.RemoveField(
            model_name='f_es_trailers',
            name='firma_oficial_seguridad',
        ),
        migrations.RemoveField(
            model_name='f_es_trailers',
            name='ine_chofer',
        ),
        migrations.RemoveField(
            model_name='f_es_trailers',
            name='n_licencia',
        ),
        migrations.RemoveField(
            model_name='f_es_trailers',
            name='n_sello',
        ),
        migrations.RemoveField(
            model_name='f_es_trailers',
            name='nombre_chofer',
        ),
        migrations.RemoveField(
            model_name='f_es_trailers',
            name='notas',
        ),
        migrations.RemoveField(
            model_name='f_es_trailers',
            name='origen',
        ),
        migrations.RemoveField(
            model_name='f_es_trailers',
            name='pedimento_caja',
        ),
        migrations.RemoveField(
            model_name='f_es_trailers',
            name='placas',
        ),
        migrations.RemoveField(
            model_name='f_es_trailers',
            name='planta',
        ),
        migrations.RemoveField(
            model_name='f_es_trailers',
            name='salida',
        ),
        migrations.RemoveField(
            model_name='f_es_trailers',
            name='transportista',
        ),
    ]
