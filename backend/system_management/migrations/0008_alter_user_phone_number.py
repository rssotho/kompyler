# Generated by Django 5.1.4 on 2025-02-01 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system_management', '0007_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
