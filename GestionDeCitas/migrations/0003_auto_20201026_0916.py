# Generated by Django 3.1.2 on 2020-10-26 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionDeCitas', '0002_auto_20201023_2317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cita',
            name='HorarioCita',
            field=models.TimeField(),
        ),
    ]
