# Generated by Django 5.0 on 2024-10-12 18:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Citas', '0051_alter_gastos_service'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageServiceImg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='...', max_length=100)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('img_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='img_service', to='Citas.serviceimage')),
                ('moment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='moment_img_service', to='Citas.momentimage')),
            ],
        ),
    ]
