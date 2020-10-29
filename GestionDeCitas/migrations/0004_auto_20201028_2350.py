# Generated by Django 3.1.2 on 2020-10-29 04:50

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('GestionDeCitas', '0003_auto_20201026_0916'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cita',
            name='EspecialidadCita',
        ),
        migrations.AddField(
            model_name='cita',
            name='DiaCita',
            field=models.DateField(default=datetime.datetime(2020, 10, 29, 4, 50, 12, 430585, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='cita',
            name='Especialidad',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='GestionDeCitas.especialidad'),
        ),
    ]
