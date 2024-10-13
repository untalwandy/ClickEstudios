# Generated by Django 5.0 on 2024-10-12 19:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Citas', '0054_momentrelatedimage_service'),
    ]

    operations = [
        migrations.AddField(
            model_name='momentimage',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='svc_img_g', to='Citas.serviceimage'),
        ),
    ]