# Generated by Django 5.1.6 on 2025-03-27 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_baihat_file_bai_hat_alter_baihat_duong_dan_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='nghesi',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
