# Generated by Django 3.1.2 on 2020-10-24 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GestionDeCitas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='Otros',
            field=models.CharField(default='', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='paciente',
            name='complemento',
            field=models.CharField(default='', max_length=50, null=True),
        ),
    ]
