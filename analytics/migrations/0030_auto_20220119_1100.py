# Generated by Django 3.1.13 on 2022-01-19 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0029_auto_20211022_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evidenciapunto',
            name='evidencia',
            field=models.FileField(null=True, upload_to='evidencia/rondines/%Y/%d/%m/'),
        ),
    ]
