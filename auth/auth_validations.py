import re
from app_shop.models import User


def validate_registration_form(name, login, password, password2, email):
    """Функция для проверки валидности данных"""
    if not (name and login and password and password2 and email):
        return "Please fill all fields."
    elif password != password2:
        return "Passwords are not equal!"
    elif len(password) < 8:
        return "Password should be at least 8 characters long."
    elif not re.search(r"\d", password) or not re.search(r"[a-zA-Z]", password):
        return "Password should contain both letters and numbers."
    elif User.query.filter_by(login=login).first():
        return "Username already exists. Please choose a different username."
    elif User.query.filter_by(email=email).first():
        return "Email is already registered. Please use a different email."
    else:
        return None
