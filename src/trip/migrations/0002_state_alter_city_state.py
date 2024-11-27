# Generated by Django 5.1.3 on 2024-11-27 00:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('abbreviation', models.CharField(max_length=2, verbose_name='Abreviatura')),
                ('country', models.CharField(max_length=100, verbose_name='País')),
            ],
        ),
        migrations.AlterField(
            model_name='city',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='trip.state', verbose_name='Provincia'),
        ),
    ]
