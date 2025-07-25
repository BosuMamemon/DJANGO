# Generated by Django 5.2.3 on 2025-06-19 01:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Board",
            fields=[
                ("idx", models.AutoField(primary_key=True, serialize=False)),
                ("writer", models.CharField(max_length=50)),
                ("title", models.CharField(max_length=200)),
                ("content", models.TextField()),
                ("hit", models.IntegerField(default=0)),
                (
                    "post_date",
                    models.DateField(blank=True, default=datetime.datetime.now),
                ),
                (
                    "file_name",
                    models.CharField(blank=True, default="", max_length=500, null=True),
                ),
                ("file_size", models.IntegerField(default=0)),
                ("down", models.IntegerField(default=0)),
            ],
        ),
    ]
