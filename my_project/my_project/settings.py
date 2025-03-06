"""
Django settings for my_project project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
import sys
import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)  # Thêm thư mục gốc vào sys.path


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-^5ykhf20%@!1rrc_j!p8(0!#5i2fv9f1rswm^8mjo+#qqq@t__'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = "common.NguoiDung"  # Đổi "ten_app" thành tên app của bạn


# Application definition


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # SMTP server của Gmail
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'lamkbvn@gmail.com'  # Email của bạn
EMAIL_HOST_PASSWORD = 'wxuudzlonenlxuun'  # Mật khẩu ứng dụng (App Password)
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# Cho phép đọc cookie từ frontend
CSRF_TRUSTED_ORIGINS = ["http://localhost:8000", "http://127.0.0.1:8000"]  # Thay bằng domain frontend của bạn
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False  # Nếu đang dùng HTTPS thì đặt True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = False  # Nếu đang dùng HTTPS thì đặt True


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'apps.common',
    'apps.nguoidung',
    'storages',  # Thêm django-storages
    'apps.loibaihatdongbo',
    'apps.nghesi',
]


# Cấu hình AWS S3
AWS_ACCESS_KEY_ID = 'admin'
AWS_SECRET_ACCESS_KEY = 'w$;8H?JFfwkAg8+'
AWS_STORAGE_BUCKET_NAME = 'spotifycloud'
AWS_S3_REGION_NAME = 'ap-southeast-2'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}


from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,  # Tạo refresh token mới khi dùng refresh
    "BLACKLIST_AFTER_ROTATION": True,  # Đưa refresh token cũ vào blacklist sau khi refresh
    "TOKEN_BLACKLIST" : True ,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "nguoi_dung_id",
    "USER_ID_CLAIM": "user_id",
    "VERIFYING_KEY": None,
    "TOKEN_TYPE_CLAIM": "token_type",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_BLACKLIST_CHECKS": True,  # Kiểm tra danh sách blacklist
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'my_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'my_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Sử dụng MySQL
        'NAME': 'spotify',  # Tên database của bạn
        'USER': 'root',  # Tên user của MySQL
        'PASSWORD': '12345abc',  # Mật khẩu của MySQL
        'HOST': 'localhost',  # Nếu dùng máy chủ từ xa, thay bằng IP hoặc domain
        'PORT': '3306',  # Cổng mặc định của MySQL
        'OPTIONS': {
            'charset': 'utf8mb4',  # Hỗ trợ tiếng Việt
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
