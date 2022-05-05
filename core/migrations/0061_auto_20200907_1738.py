# Generated by Django 2.2.4 on 2020-09-07 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0060_permrol_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='planta',
            name='status',
            field=models.CharField(blank=True, choices=[('relevante', 'Relevante'), ('optimo', 'Óptimo')], default='optimo', max_length=50, null=True),
        ),
    ]
