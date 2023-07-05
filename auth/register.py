from flask import (
    Blueprint, flash, redirect, render_template, request, url_for
)
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash, generate_password_hash

from app_shop import db, manager
from app_shop.models import User
from auth.auth_validations import validate_registration_form
from config import EMAIL_SUPERUSER, LOGIN_NAME_SUPERUSER, PASSWORD_SUPERUSER

auth_bp = Blueprint('auth', __name__, template_folder='templates', static_folder='static')


@auth_bp.route('/register', methods=('GET', 'POST'))
def register_page():
    """Страница регистрации пользователя"""
    # Проверка, существует ли уже суперпользователь
    if not User.query.filter_by(login={LOGIN_NAME_SUPERUSER}).first():
        try:
            # Создание суперпользователя
            superuser = User(
                login=LOGIN_NAME_SUPERUSER,
                name='Сергей',
                password=generate_password_hash(PASSWORD_SUPERUSER),
                email=EMAIL_SUPERUSER,
                is_admin=True
            )
            db.session.add(superuser)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            print('Ошибка при создании суперпользователя:', str(e))

    if request.method == "POST":
        name = request.form.get("name")
        login = request.form.get("login")
        password = request.form.get('password')
        password2 = request.form.get('password2')
        email = request.form.get('email')

        error = validate_registration_form(name, login, password, password2, email)
        if error:
            flash(error)
        else:
            try:
                new_user = User(
                    login=login,
                    name=name,
                    password=generate_password_hash(password),
                    email=email
                )
                db.session.add(new_user)
                db.session.commit()
                flash("Registration successful. You can now login.")
                return redirect(url_for('.login_page'))
            except SQLAlchemyError as e:
                db.session.rollback()
                print('Ошибка при создании суперпользователя:', str(e))

    return render_template('register.html')


@auth_bp.route('/login', methods=('GET', 'POST'))
def login_page():
    """Страница логина Юзера"""
    if current_user.is_authenticated:
        return redirect('basket.html')
    login = request.form.get("login")
    password = request.form.get("password")
    if request.method == 'POST':
        if login and password:
            user = User.query.filter_by(login=login).first()

            if user and check_password_hash(user.password, password):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('blog.index_page'))
            else:
                flash('Login or password are incorrect')
        else:
            flash('Please fill in login and password')
    return render_template('login.html')


@manager.user_loader
def load_user(user_id):
    """Загрузчик для работы с сессией"""
    return User.query.get(user_id)


@auth_bp.route("/logout")
@login_required
def logout_page():
    """Страница выхода Юзера"""
    logout_user()
    return redirect(url_for('auth.login_page'))
