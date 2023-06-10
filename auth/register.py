from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from app_shop import db
from app_shop.models import User

auth_bp = Blueprint('auth', __name__, template_folder='templates', static_folder='static')


@auth_bp.route('/')
def index_auth():
    return 'auth'


@auth_bp.route('/register', methods=('GET', 'POST'))
def register_page():
    if request.method == "POST":
        name = request.form.get("name")
        login = request.form.get("login")
        password = request.form.get('password')
        password2 = request.form.get('password2')
        email_field = request.form.get('email')

        if not (name and login and password and password2 and email_field):
            flash("Please fill all fields")
        elif password != password2:
            flash("Passwords are not equal!")
        else:
            existing_user = User.query.filter_by(login=login).first()
            if existing_user:
                flash("Username already exists. Please choose a different username.")
            else:
                new_user = User(login=login, name=name, password=generate_password_hash(password), email=email_field)
                db.session.add(new_user)
                db.session.commit()
                flash("Registration successful. You can now login.")
                return redirect(url_for('.login_page'))

    return render_template('register.html')


@auth_bp.route('/login', methods=('GET', 'POST'))
def login_page():
    login = request.form.get("login")
    password = request.form.get("password")
    if request.method == 'POST':
        if login and password:
            user = User.query.filter_by(login=login).first()

            if user and check_password_hash(user.password, password):
                login_user(user)
                next_page = request.args.get('next')
                return redirect(next_page or url_for('index'))
            else:
                flash('Login or password are incorrect')
        else:
            flash('Please fill in login and password')
    return render_template('login.html')



@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
