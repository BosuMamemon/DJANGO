# Generated by Django 5.2.3 on 2025-06-13 07:56

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
                ("title", models.CharField(max_length=100)),
                ("content", models.TextField()),
            ],
        ),
    ]
