# Generated by Django 4.2.6 on 2024-02-09 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manage_account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmer',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='manage_account/profile_pic/'),
        ),
    ]
