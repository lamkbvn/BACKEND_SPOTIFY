# Generated by Django 5.1.6 on 2025-03-06 15:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaiHat',
            fields=[
                ('bai_hat_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ten_bai_hat', models.CharField(max_length=255)),
                ('nghe_si', models.CharField(max_length=255)),
                ('ten_album', models.CharField(blank=True, max_length=255, null=True)),
                ('the_loai', models.CharField(max_length=100)),
                ('duong_dan', models.URLField()),
                ('loi_bai_hat', models.TextField(blank=True, null=True)),
                ('thoi_luong', models.IntegerField()),
                ('ngay_phat_hanh', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='GoiPremium',
            fields=[
                ('goi_premium_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ten_goi', models.CharField(max_length=100)),
                ('gia', models.DecimalField(decimal_places=2, max_digits=10)),
                ('thoi_han', models.IntegerField()),
                ('mo_ta', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LoaiBaiHat',
            fields=[
                ('loai_bai_hat_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ten_loai', models.CharField(help_text='Tên loại bài hát (Pop, Rock, Ballad,...)', max_length=255, unique=True)),
                ('mo_ta', models.TextField(blank=True, help_text='Mô tả về loại bài hát', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='NgheSi',
            fields=[
                ('nghe_si_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ten_nghe_si', models.CharField(max_length=255, unique=True)),
                ('tieu_su', models.TextField(blank=True, null=True)),
                ('anh_dai_dien', models.URLField(blank=True, null=True)),
                ('ngay_sinh', models.DateField(blank=True, null=True)),
                ('quoc_gia', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='NguoiDung',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('nguoi_dung_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('so_dien_thoai', models.CharField(blank=True, max_length=15, null=True)),
                ('ten_hien_thi', models.CharField(max_length=100)),
                ('avatar_url', models.URLField(blank=True, null=True)),
                ('ngay_sinh', models.DateField(blank=True, null=True)),
                ('quoc_gia', models.CharField(blank=True, max_length=50, null=True)),
                ('la_premium', models.BooleanField(default=False)),
                ('google_id', models.CharField(blank=True, max_length=255, null=True)),
                ('facebook_id', models.CharField(blank=True, max_length=255, null=True)),
                ('ngay_tao', models.DateTimeField(auto_now_add=True)),
                ('ngay_cap_nhat', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'nguoidung',
            },
        ),
        migrations.CreateModel(
            name='BaiHatYeuThich',
            fields=[
                ('bai_hat_yeu_thich_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ngay_them', models.DateTimeField(auto_now_add=True)),
                ('bai_hat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.baihat')),
                ('nguoi_dung', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DanhSachPhat',
            fields=[
                ('dach_sach_phat_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ten_danh_sach', models.CharField(max_length=255)),
                ('mo_ta', models.TextField(blank=True, null=True)),
                ('la_cong_khai', models.BooleanField(default=True)),
                ('ngay_tao', models.DateTimeField(auto_now_add=True)),
                ('tong_thoi_luong', models.IntegerField(default=0)),
                ('so_thu_tu', models.IntegerField(null=True)),
                ('anh_danh_sach', models.URLField(default='http://localhost:5173/uifaces-popular-image%20(1).jpg')),
                ('so_nguoi_theo_doi', models.IntegerField(default=0)),
                ('nguoi_dung_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['so_thu_tu'],
            },
        ),
        migrations.CreateModel(
            name='BaiHatTrongDanhSach',
            fields=[
                ('bai_hat_trong_danh_sach_id', models.AutoField(primary_key=True, serialize=False)),
                ('ngay_them', models.DateTimeField(auto_now_add=True)),
                ('bai_hat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.baihat')),
                ('danh_sach_phat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.danhsachphat')),
            ],
        ),
        migrations.CreateModel(
            name='LichSuNghe',
            fields=[
                ('lich_su_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('thoi_gian_nghe', models.DateTimeField(auto_now_add=True)),
                ('thoi_luong_nghe', models.IntegerField()),
                ('bai_hat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.baihat')),
                ('nguoi_dung', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LoiBaiHatDongBo',
            fields=[
                ('loi_dong_bo_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('loi_doan', models.CharField(max_length=255)),
                ('thoi_gian_bat_dau', models.DecimalField(decimal_places=2, max_digits=6)),
                ('thoi_gian_ket_thuc', models.DecimalField(decimal_places=2, max_digits=6)),
                ('bai_hat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.baihat')),
            ],
        ),
        migrations.CreateModel(
            name='TaiXuong',
            fields=[
                ('tai_xuong_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ngay_tai_xuong', models.DateTimeField(auto_now_add=True)),
                ('bai_hat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.baihat')),
                ('nguoi_dung', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ThanhToan',
            fields=[
                ('thanh_toan_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('ngay_thanh_toan', models.DateTimeField(auto_now_add=True)),
                ('phuong_thuc', models.CharField(max_length=50)),
                ('so_tien', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ngay_het_han', models.DateTimeField()),
                ('tu_dong_gia_han', models.BooleanField(default=False)),
                ('goi_premium', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.goipremium')),
                ('nguoi_dung', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
