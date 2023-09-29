# Generated by Django 4.1.5 on 2023-05-31 10:05

import app_data.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_data", "0011_delete_filtertable"),
    ]

    operations = [
        migrations.AlterField(
            model_name="registration",
            name="profile",
            field=models.ImageField(
                default="assets/media/default-avatar.jpg",
                null=True,
                upload_to=app_data.models.getFileNameProfile,
            ),
        ),
    ]