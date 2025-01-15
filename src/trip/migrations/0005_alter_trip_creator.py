# Generated by Django 5.1.3 on 2024-12-23 14:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0004_trip_creator'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_trips', to=settings.AUTH_USER_MODEL, verbose_name='Creador'),
        ),
    ]
