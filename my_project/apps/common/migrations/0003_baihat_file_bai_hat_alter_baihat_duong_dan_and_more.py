# Generated by Django 5.1.6 on 2025-03-20 12:12

import storages.backends.s3
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0002_nguoidung_gioi_tinh"),
    ]

    operations = [
        migrations.AddField(
            model_name="baihat",
            name="file_bai_hat",
            field=models.FileField(
                blank=True,
                null=True,
                storage=storages.backends.s3.S3Storage(),
                upload_to="songs/",
            ),
        ),
        migrations.AlterField(
            model_name="baihat",
            name="duong_dan",
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="nguoidung",
            name="ngay_sinh",
            field=models.DateField(blank=True, default="2004-08-03"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="nguoidung",
            name="so_dien_thoai",
            field=models.CharField(blank=True, default="0000000000", max_length=15),
            preserve_default=False,
        ),
    ]
