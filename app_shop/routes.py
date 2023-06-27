from flask import render_template, url_for, redirect, request, Blueprint
from random import sample
from sqlalchemy.orm import joinedload
from app_shop import toolbar

from app_shop import redis
from app_shop.models import Game, Genre, Developer, Publisher, db

bp = Blueprint('blog', __name__)


@bp.route('/redis')
def redis_():
    """"Подключенния и тест redis"""
    # Пример использования: сохранение значения в Redis
    redis.set('key', 'Redis_Value')

    # Пример использования: получение значения из Redis
    value = redis.get('key')

    return value


@bp.route('/debug')
def debug():
    # Дополнительный маршрут для отображения отладочной панели
    return toolbar.send_static_file('debug_toolbar.js')


@bp.route('/')
def index_page():
    """Главная страница"""

    all_games = Game.query.all()
    random_games = sample(all_games, 6)
    return render_template('shop/index.html', all_games=random_games)


@bp.route('/shop_games')
@bp.route('/genre/<gerne_name>')
def all_game_page(gerne_name=None):
    """Страница с товарами все и отдельно по категориям"""
    page = request.args.get('page', 1, type=int)
    per_page = 6  # Количество игр на странице

    games_query = Game.query.options(joinedload(Game.publisher), joinedload(Game.developer))

    if gerne_name:
        games_query = games_query.join(Game.genres).filter(Genre.name == gerne_name)

    games_pagination = games_query.paginate(page=page, per_page=per_page)

    return render_template('shop/games.html', games_pagination=games_pagination)


@bp.route('/contact')
def contact():
    """Обратная связ"""
    return render_template('shop/contact.html')


@bp.after_request
def redirect_to(response):
    if response.status_code == 401:
        return redirect(url_for('auth.login_page') + '?next=' + request.url)
    return response


@bp.route('/add_game', methods=['GET', 'POST'])
def add_game():
    if request.method == 'POST':
        game_name = request.form['game_name']
        game_price = request.form['game_price']
        game_developer_name = request.form['game_developers']
        game_publisher_name = request.form['game_publishers']
        game_genres = [name.strip() for name in request.form['game_genres'].split(',')]
        game_description = request.form['game_description']
        game_photo = request.form['game_photo']
        game_twitch_stream = request.form['game_twitch_stream']

        # Поиск или создание разработчика
        developer = Developer.query.filter_by(name=game_developer_name).first()
        if not developer:
            developer = Developer(name=game_developer_name)
            db.session.add(developer)

        # Поиск или создание издателя
        publisher = Publisher.query.filter_by(name=game_publisher_name).first()
        if not publisher:
            publisher = Publisher(name=game_publisher_name)
            db.session.add(publisher)

        # Создание и сохранение игры в базе данных
        game = Game(name=game_name, price=game_price, description=game_description,
                    photo=game_photo, twitch_stream=game_twitch_stream)
        game.developer = developer
        game.publisher = publisher

        # Поиск или создание жанров и связывание их с игрой
        for genre_name in game_genres:
            genre = Genre.query.filter_by(name=genre_name).first()
            if not genre:
                genre = Genre(name=genre_name)
                db.session.add(genre)
            game.genres.append(genre)

        db.session.add(game)
        db.session.commit()

        return redirect(url_for('blog.add_game'))
    else:
        return render_template('shop/add_game.html')
