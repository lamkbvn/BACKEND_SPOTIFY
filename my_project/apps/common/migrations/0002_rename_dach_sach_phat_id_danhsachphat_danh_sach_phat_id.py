# Generated by Django 5.1.6 on 2025-03-07 04:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='danhsachphat',
            old_name='dach_sach_phat_id',
            new_name='danh_sach_phat_id',
        ),
    ]
