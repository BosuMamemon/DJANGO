# Generated by Django 5.2.4 on 2025-07-07 03:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("test_app", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="post",
            old_name="create_at",
            new_name="created_at",
        ),
    ]
