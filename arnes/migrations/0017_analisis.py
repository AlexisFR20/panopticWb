# Generated by Django 3.1.13 on 2022-02-04 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('arnes', '0016_auto_20201022_0854'),
    ]

    operations = [
        migrations.CreateModel(
            name='Analisis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
    ]
