from django.db import models

class NguoiDung(models.Model):
    nguoi_dung_id = models.BigAutoField(primary_key=True )  # Khóa chính, tự động tăng
    email = models.EmailField(unique=True)
    so_dien_thoai = models.CharField(max_length=15, blank=True, null=True)
    mat_khau = models.CharField(max_length=255)
    ten_hien_thi = models.CharField(max_length=100)
    avatar_url = models.URLField(blank=True, null=True)
    ngay_sinh = models.DateField(blank=True, null=True)
    quoc_gia = models.CharField(max_length=50, blank=True, null=True)
    la_premium = models.BooleanField(default=False)
    google_id = models.CharField(max_length=255, blank=True, null=True)
    facebook_id = models.CharField(max_length=255, blank=True, null=True)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    ngay_cap_nhat = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nguoi_dung_id


class BaiHat(models.Model):
    bai_hat_id  =  models.BigAutoField(primary_key=True )  # Khóa chính, tự động tăng
    ten_bai_hat = models.CharField(max_length=255)
    nghe_si = models.CharField(max_length=255)
    ten_album = models.CharField(max_length=255, blank=True, null=True)
    the_loai = models.CharField(max_length=100)
    duong_dan = models.URLField()
    loi_bai_hat = models.TextField(blank=True, null=True)
    thoi_luong = models.IntegerField()  # Tính bằng giây
    ngay_phat_hanh = models.DateField()

    def __str__(self):
        return self.bai_hat_id


class DanhSachPhat(models.Model):
    dach_sach_phat_id =  models.BigAutoField(primary_key=True )  # Khóa chính, tự động tăng
    nguoi_dung_id = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    ten_danh_sach = models.CharField(max_length=255)
    mo_ta = models.TextField(blank=True, null=True)
    la_cong_khai = models.BooleanField(default=True)
    ngay_tao = models.DateTimeField(auto_now_add=True)
    tong_thoi_luong = models.IntegerField(default=0)  # Tính bằng giây

    def __str__(self):
        return self.dach_sach_phat_id

class LoiBaiHatDongBo(models.Model):
    loi_dong_bo_id =  models.BigAutoField(primary_key=True )  # Khóa chính, tự động tăng
    bai_hat = models.ForeignKey(BaiHat, on_delete=models.CASCADE)
    loi_doan = models.CharField(max_length=255)
    thoi_gian_bat_dau = models.DecimalField(max_digits=6, decimal_places=2)
    thoi_gian_ket_thuc = models.DecimalField(max_digits=6, decimal_places=2)



class BaiHatTrongDanhSach(models.Model):
    bai_hat_trong_danh_sach_id =  models.AutoField(primary_key=True )  # Khóa chính, tự động tăng
    danh_sach_phat = models.ForeignKey(DanhSachPhat, on_delete=models.CASCADE)
    bai_hat = models.ForeignKey(BaiHat, on_delete=models.CASCADE)
    ngay_them = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bai_hat_trong_danh_sach_id

class BaiHatYeuThich(models.Model):
    bai_hat_yeu_thich_id =  models.BigAutoField(primary_key=True )  # Khóa chính, tự động tăng
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    bai_hat = models.ForeignKey(BaiHat, on_delete=models.CASCADE)
    ngay_them = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.bai_hat_yeu_thich_id

class LichSuNghe(models.Model):
    lich_su_id =   models.BigAutoField(primary_key=True )  # Khóa chính, tự động tăng
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    bai_hat = models.ForeignKey(BaiHat, on_delete=models.CASCADE)
    thoi_gian_nghe = models.DateTimeField(auto_now_add=True)
    thoi_luong_nghe = models.IntegerField()  # Tính bằng giây

    def __str__(self):
        return self.lich_su_id

class GoiPremium(models.Model):
    goi_premium_id =  models.BigAutoField(primary_key=True )  # Khóa chính, tự động tăng
    ten_goi = models.CharField(max_length=100)
    gia = models.DecimalField(max_digits=10, decimal_places=2)
    thoi_han = models.IntegerField()  # Tính bằng ngày
    mo_ta = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.goi_premium_id

class ThanhToan(models.Model):
    thanh_toan_id =  models.BigAutoField(primary_key=True )  # Khóa chính, tự động tăng
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    goi_premium = models.ForeignKey(GoiPremium, on_delete=models.CASCADE)
    ngay_thanh_toan = models.DateTimeField(auto_now_add=True)
    phuong_thuc = models.CharField(max_length=50)
    so_tien = models.DecimalField(max_digits=10, decimal_places=2)
    ngay_het_han = models.DateTimeField()
    tu_dong_gia_han = models.BooleanField(default=False)

    def __str__(self):
        return self.thanh_toan_id

class TaiXuong(models.Model):
    tai_xuong_id =  models.BigAutoField(primary_key=True )  # Khóa chính, tự động tăng
    nguoi_dung = models.ForeignKey(NguoiDung, on_delete=models.CASCADE)
    bai_hat = models.ForeignKey(BaiHat, on_delete=models.CASCADE)
    ngay_tai_xuong = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tai_xuong_id
