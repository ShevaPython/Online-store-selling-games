from app_shop import app
from flask import render_template, url_for
from app_shop.models import Game



@app.route('/index')
def index():
    return render_template('shop/index.html')


@app.route('/base')
def base():
    print(url_for('base'))
    return render_template('base.html')





@app.route('/all_game')
def all_game_page():
    games= Game.query.all()
    return render_template('shop/show_all_games.html', games=games)
