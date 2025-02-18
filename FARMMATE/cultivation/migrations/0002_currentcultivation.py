# Generated by Django 4.2.6 on 2024-02-11 15:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cultivation', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentCultivation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=50)),
                ('product_id', models.CharField(max_length=50, unique=True)),
                ('status', models.CharField(max_length=20)),
                ('location', models.CharField(max_length=300)),
                ('cultivated_area', models.CharField(max_length=30)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('harvested_date', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'current_cultivation',
            },
        ),
    ]
