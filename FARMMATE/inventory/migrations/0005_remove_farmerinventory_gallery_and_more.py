# Generated by Django 4.2.6 on 2024-02-24 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_alter_inventorygallery_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='farmerinventory',
            name='gallery',
        ),
        migrations.DeleteModel(
            name='InventoryGallery',
        ),
    ]
