# Generated by Django 4.2.6 on 2023-10-12 01:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Animal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nickname",
                    models.CharField(max_length=8, null=True, verbose_name="반려동물 이름"),
                ),
                ("main_img_id", models.IntegerField(default=-1)),
                (
                    "main_img",
                    models.CharField(blank=True, default="", max_length=255, null=True),
                ),
                ("is_missing", models.BooleanField(default=False)),
                ("register_date", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "db_table": "Animal",
            },
        ),
        migrations.CreateModel(
            name="AnimalImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_learning", models.BooleanField(default=False)),
                ("register_date", models.DateTimeField(auto_now_add=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True, upload_to="animal", verbose_name="동물 사진"
                    ),
                ),
                (
                    "animal_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="animal.animal"
                    ),
                ),
            ],
            options={
                "db_table": "Animal_Image",
            },
        ),
    ]
