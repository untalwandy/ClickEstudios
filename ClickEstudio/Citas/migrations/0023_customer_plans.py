# Generated by Django 5.0.6 on 2024-06-17 00:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Citas', '0022_alter_customer_plan_choice'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='plans',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='plans_customer', to='Citas.plans'),
        ),
    ]
