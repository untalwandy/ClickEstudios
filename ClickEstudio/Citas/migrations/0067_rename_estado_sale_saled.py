# Generated by Django 5.0 on 2024-10-25 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Citas', '0066_sale_reserve_alter_sale_cliente_alter_sale_plan'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='estado',
            new_name='saled',
        ),
    ]