# Generated by Django 5.0.6 on 2024-06-26 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Citas', '0029_role_usera'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='description',
            field=models.TextField(default='Un rol indefinodo podría tener la capacidad de ver ciertos contenidos que no requieran permisos especiales, como páginas informativas o recursos de ayuda y mas'),
        ),
    ]