# Generated by Django 5.0.7 on 2024-08-17 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Citas', '0036_rename_content_tweet_title_remove_tweet_user_tweet_p_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='imgtweet',
            name='img_tweet',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]