# Generated by Django 4.2.6 on 2023-11-14 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("animal", "0003_animal_characteristic"),
    ]

    operations = [
        migrations.AddField(
            model_name="animal",
            name="missing_location",
            field=models.CharField(default="", max_length=500),
        ),
    ]