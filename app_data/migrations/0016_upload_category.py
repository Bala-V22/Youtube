# Generated by Django 4.1.5 on 2023-06-09 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_data", "0015_alter_login_user_uid_alter_login_user_user_mail"),
    ]

    operations = [
        migrations.AddField(
            model_name="upload",
            name="category",
            field=models.CharField(
                choices=[("gaming", "Gaming"), ("education", "Education")],
                max_length=30,
                null=True,
            ),
        ),
    ]