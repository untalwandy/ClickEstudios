# Generated by Django 5.0.6 on 2024-06-11 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Citas', '0012_momentrelatedimage_img_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='momentrelatedimage',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='moment_related_images/'),
        ),
    ]