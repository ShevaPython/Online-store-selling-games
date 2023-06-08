from flask import Blueprint
import functools

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

auth_bp = Blueprint('auth', __name__, template_folder='templates', static_folder='static')


@auth_bp.route('/')
def index_auth():
    return 'auth'


@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    # if request.method == 'POST':
    #     username = request.form['username']
    #     password = request.form['password']
    #     error = None
    #
    #     if not username:
    #         error = 'Username is required.'
    #     elif not password:
    #         error = 'Password is required.'
    #
    #     if error is None:
    #         try:
    #             db.execute(
    #                 "INSERT INTO user (username, password) VALUES (?, ?)",
    #                 (username, generate_password_hash(password)),
    #             )
    #             db.commit()
    #         except db.IntegrityError:
    #             error = f"User {username} is already registered."
    #         else:
    #             return redirect(url_for("auth.login"))
    #
    #     flash(error)

    return render_template('register.html')
