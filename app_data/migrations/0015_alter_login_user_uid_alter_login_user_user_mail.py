# Generated by Django 4.1.5 on 2023-06-08 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_data", "0014_alter_upload_description_alter_upload_image_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="login_user",
            name="uid",
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="login_user",
            name="user_mail",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
