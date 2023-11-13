# Generated by Django 4.2.6 on 2023-11-14 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("posts", "0004_missingimage"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="postimage",
            name="image_id",
        ),
        migrations.AddField(
            model_name="postimage",
            name="image",
            field=models.ImageField(
                blank=True, upload_to="post", verbose_name="post 사진"
            ),
        ),
    ]
