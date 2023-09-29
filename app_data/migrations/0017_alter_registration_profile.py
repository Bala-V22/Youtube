# Generated by Django 4.1.5 on 2023-06-10 10:33

import app_data.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_data", "0016_upload_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="registration",
            name="profile",
            field=models.ImageField(
                default="static/assets/media/default-avatar.jpg",
                null=True,
                upload_to=app_data.models.getFileNameProfile,
            ),
        ),
    ]
