# Generated by Django 5.1.6 on 2025-03-31 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0005_album_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="baihat",
            name="is_premium",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
