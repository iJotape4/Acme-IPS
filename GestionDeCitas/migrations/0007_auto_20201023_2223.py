# Generated by Django 3.1.2 on 2020-10-24 03:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GestionDeCitas', '0006_auto_20201022_2159'),
    ]

    operations = [
        migrations.CreateModel(
            name='Especialidad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('HorarioLlegada', models.TimeField()),
                ('HoraioSalida', models.TimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='medico',
            name='Especialidad',
        ),
        migrations.RemoveField(
            model_name='medico',
            name='HoraioSalida',
        ),
        migrations.RemoveField(
            model_name='medico',
            name='HorarioLlegada',
        ),
        migrations.AddField(
            model_name='medico',
            name='especialidad',
            field=models.ForeignKey(default='general', on_delete=django.db.models.deletion.CASCADE, to='GestionDeCitas.especialidad'),
        ),
        migrations.AddField(
            model_name='medico',
            name='horario',
            field=models.ForeignKey(default=(0, 0, 0, 0), on_delete=django.db.models.deletion.CASCADE, to='GestionDeCitas.horario'),
        ),
    ]
