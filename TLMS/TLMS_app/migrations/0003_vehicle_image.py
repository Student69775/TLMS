# Generated by Django 4.2.16 on 2024-11-19 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TLMS_app', '0002_vehicle_driver_consignment'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='vehicle_images/'),
        ),
    ]
