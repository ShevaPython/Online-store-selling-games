from app_shop import app
from flask import render_template, url_for, redirect, request
from app_shop.models import Game, Genre, GamesGenres
from app_shop import db


@app.route('/')
def index_page():
    games = Game.query.all()
    return render_template('shop/index.html',games=games)


@app.route('/shop_games')
def all_game_page():

    all_games = Game.query.all()
    return render_template('shop/games.html', all_games=all_games)


@app.route('/genre/<gerne_name>')
def search_genre(gerne_name):

    all_games = db.session.query(Game).join(GamesGenres, GamesGenres.game_id == Game.id).join(Genre,
                                                                                              Genre.id == GamesGenres.genre_id).filter(
        Genre.name == gerne_name).all()

    return render_template('shop/games.html', all_games=all_games)


@app.route('/contact')
def contact():

    return render_template('shop/contact.html')


@app.after_request
def redirect_to(response):
    if response.status_code == 401:
        return redirect(url_for('auth.login_page') + '?next=' + request.url)
    return response
