# 🎧 Ứng dụng Spotify Clone

Đây là một ứng dụng clone Spotify được xây dựng bằng **Django REST Framework** cho phía Backend và **ReactJS** cho phía Frontend. Ứng dụng hỗ trợ phát nhạc trực tuyến, quản lý người dùng, playlist cá nhân, giao diện hiện đại và nhiều tính năng tương tự Spotify.

---

## 📌 Tính năng nổi bật

### 🔐 Xác thực người dùng
- Đăng ký / Đăng nhập / Đăng xuất
- Trang quản trị riêng cho admin

### 🎵 Trình phát nhạc
- Phát / Tạm dừng / Tua
- Thanh tiến trình bài hát
- Chuyển bài / Phát lại / Phát ngẫu nhiên
- Chặn chuyển bài khi là quảng cáo

### 🧑‍💼 Tính năng người dùng
- Xem và chỉnh sửa hồ sơ cá nhân
- Khám phá nhạc theo thể loại, xu hướng
- Tạo và quản lý playlist

### 🛠️ Quản trị (Admin)
- Quản lý người dùng, bài hát, album, nghệ sĩ, thống kê
- Giao diện dành riêng cho admin
---

## 🧱 Công nghệ sử dụng

### ⚙️ Backend (Django)

- **Django 5** + **Django REST Framework**: Xây dựng API backend.
- **Django Channels** + **Daphne**: Hỗ trợ tính năng realtime (chat, thông báo).
- **MySQL**: Cơ sở dữ liệu chính.
- **Cloudinary + AWS S3**: Lưu trữ ảnh và file âm thanh.


### 🎧 Frontend (ReactJS)

- **React + TypeScript**: Xây dựng giao diện người dùng mạnh mẽ, an toàn.
- **Redux Toolkit**: Quản lý trạng thái ứng dụng hiện đại, đơn giản hóa logic.
- **React Router DOM**: Điều hướng giữa các trang một cách mượt mà.
- **Ant Design UI**: Sử dụng bộ component UI đẹp mắt và tiện dụng.

---

## ⚙️ Cài đặt

### 1. Backend - Django

```bash
git clone https://github.com/lamkbvn/BACKEND_SPOTIFY.git
cd BACKEND_SPOTIFY/my_project
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 2. Frontend - React
```bash
git clone https://github.com/duylam15/react-clone-spotify.git
cd react-clone-spotify
npm install
npm run dev
