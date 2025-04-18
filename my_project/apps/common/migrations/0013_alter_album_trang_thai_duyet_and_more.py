# Generated by Django 5.1.6 on 2025-04-11 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0012_merge_20250411_1127"),
    ]

    operations = [
        migrations.AlterField(
            model_name="album",
            name="trang_thai_duyet",
            field=models.CharField(
                choices=[
                    ("pending", "Chờ duyệt"),
                    ("approved", "Đã duyệt"),
                    ("rejected", "Bị từ chối"),
                ],
                default="approved",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="baihat",
            name="trang_thai_duyet",
            field=models.CharField(
                choices=[
                    ("pending", "Chờ duyệt"),
                    ("approved", "Đã duyệt"),
                    ("rejected", "Bị từ chối"),
                ],
                default="approved",
                max_length=20,
            ),
        ),
    ]
