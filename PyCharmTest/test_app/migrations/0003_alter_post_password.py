# Generated by Django 5.2.4 on 2025-07-07 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("test_app", "0002_rename_create_at_post_created_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="password",
            field=models.CharField(max_length=128, verbose_name="비밀번호"),
        ),
    ]
