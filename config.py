from dotenv import load_dotenv
import os

load_dotenv()

# База данных
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# Секретный ключ
SECRET_KEY = os.getenv("SECRET_KEY")

# Данные суперпользователя

LOGIN_NAME_SUPERUSER = os.getenv("LOGIN_NAME_SUPERUSER")
PASSWORD_SUPERUSER = os.getenv("PASSWORD_SUPERUSER")
EMAIL_SUPERUSER = os.getenv("EMAIL_SUPERUSER")

# Платежная система
LIQPAY_PUBLIC = os.getenv("LIQPAY_PUBLIC")
LIQPAY_PRIVATE = os.getenv("LIQPAY_PRIVATE")

# gmailpassword
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")
