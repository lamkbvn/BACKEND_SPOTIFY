# Generated by Django 5.1.6 on 2025-03-14 10:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0003_bangxephangbaihat"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="baihat",
            name="ten_album",
        ),
        migrations.AlterField(
            model_name="baihat",
            name="nghe_si",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="bai_hat",
                to="common.nghesi",
            ),
        ),
        migrations.CreateModel(
            name="Album",
            fields=[
                ("album_id", models.BigAutoField(primary_key=True, serialize=False)),
                ("ten_album", models.CharField(max_length=255, unique=True)),
                ("anh_bia", models.URLField(blank=True, null=True)),
                ("ngay_phat_hanh", models.DateField()),
                ("the_loai", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "nghe_si",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="albums",
                        to="common.nghesi",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="baihat",
            name="album",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="bai_hat",
                to="common.album",
            ),
        ),
    ]
