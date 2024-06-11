# Generated by Django 5.0.6 on 2024-06-10 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Citas', '0004_alter_customer_dni_alter_customer_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MomentImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Momento', max_length=255)),
                ('image', models.ImageField(upload_to='moment_images/')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Servicio', max_length=255)),
                ('image', models.ImageField(upload_to='service_images/')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
