from app_shop import app
from flask import render_template, url_for, redirect, request
from app_shop.models import Game, Genre


@app.route('/')
def index_page():
    genres = Genre.query.all()
    return render_template('shop/index.html', genres=genres)



@app.route('/base')
def base():
    genres = Genre.query.all()
    return render_template('base.html', genres=genres)


@app.route('/all_game')
def all_game_page():
    all_games = Game.query.all()
    genres = Genre.query.all()

    return render_template('shop/show_all_games.html', all_games=all_games, genres=genres)


@app.after_request
def redirect_to(response):
    if response.status_code == 401:
        return redirect(url_for('auth.login_page') + '?next=' + request.url)
    return response
