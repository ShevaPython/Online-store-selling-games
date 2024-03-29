from flask import render_template, url_for, redirect, request, Blueprint, flash
from random import sample
from sqlalchemy.orm import joinedload
from app_shop import toolbar
from app_shop import mail
from flask_mail import Message

from app_shop import redis
from app_shop.models import Game, Genre, Developer, Publisher, db
from app_shop.helpers.is_valid_email import is_valid_email

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


from random import sample

@bp.route('/')
def index_page():
    """Главная страница"""

    all_games = Game.query.all()

    # Проверяем, что список не пустой
    if not all_games:
        random_games = []
    else:
        # В противном случае, выбираем случайные игры
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




@bp.route('/show_one_game', methods=['GET'])
def show_one_game():
    search_query = request.args.get('search', '')
    game = Game.query.filter(Game.name.ilike(f"%{search_query}%")).first()
    if game is not None:
        return render_template('shop/show_one_game.html',game=game)
    else:
        return render_template('shop/error_404.html')

@bp.route('/game/<game_name>')
def one_game(game_name):
    # Получите данные игры на основе переданного имени
    game = Game.query.filter_by(name=game_name).first()

    if game:
        # Если игра найдена, отобразите шаблон с детальной информацией об игре
        return render_template('shop/show_one_game.html', game=game)
    else:
        # Если игра не найдена, перенаправьте пользователя на страницу 404
        return redirect(url_for('error_404'))



@bp.route('/send_mail', methods=['POST'])
def send_mail():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        message = request.form.get('message')
        try:

            if not username or not email or not message:
                flash('Please fill in all the fields.', 'error')
                return redirect(url_for('blog.contact'))

            if not is_valid_email(email):
                flash('Please enter a valid email address.', 'error')
                return redirect(url_for('blog.contact'))

            msg = Message('New Message from Contact Form',
                          sender=email,
                          recipients=['shevadotka@gmail.com'])

            msg.body = f"Name: {username}\nEmail: {email}\n\n{message}"
            mail.send(msg)
            flash('Your message has been sent!', 'success')
            return redirect(url_for('blog.contact'))
        except Exception as e:
            flash('An error occurred while sending the message. Please try again later.', 'error')

    return render_template('shop/contact.html')
