from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class Developer(db.Model):
    """Модель Дквелопер"""
    __tablename__ = 'developer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False, index=True)
    description = db.Column(db.String(400), nullable=True)
    developer_site = db.Column(db.String(45), nullable=True)
    # Отношение один-ко-многим с таблицей Games
    games = db.relationship('Game', backref='developer', lazy='select')

    def __repr__(self):
        return F"{self.name}"


class Publisher(db.Model):
    """Модель Издатель"""
    __tablename__ = 'publisher'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False, index=True)
    description = db.Column(db.String(400), nullable=True)
    publisher_site = db.Column(db.String(45), nullable=True)

    # Отношение один-ко-многим с таблицей Games
    games = db.relationship('Game', backref='publisher', lazy='select')

    def __repr__(self):
        return F"{self.name}"


class GamesGenres(db.Model):
    """Многие  ко многим жанры игры"""
    __tablename__ = 'games_genres'
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True, index=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), primary_key=True, index=True)


class Game(db.Model):
    """Модель Игра"""
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False, unique=True, index=True)
    price = db.Column(db.Integer, nullable=False, index=True)
    developer_id = db.Column(db.Integer, db.ForeignKey('developer.id'), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'), nullable=False)
    photo = db.Column(db.String(200), nullable=True, index=True)
    description=db.Column(db.String(500),nullable=True)
    # Отношение многие-ко-многим с моделью Genre
    genres = db.relationship('Genre', secondary='games_genres', lazy='joined',
                             backref=db.backref('games', lazy=True))
    twitch_stream = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return F"{self.name}"

class Genre(db.Model):
    """Модель Жанр"""
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False, index=True)

    def __repr__(self):
        return F"{self.name}"


class User(db.Model, UserMixin):
    """Модель Юзер"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    login = db.Column(db.String(255), unique=True, index=True)
    email = db.Column(db.String(255), unique=True, index=True)
    password = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean(), default=False)
    confirmed_at = db.Column(db.DateTime, default=datetime.utcnow)
    # Отношение один-ко-многим с таблицей Orders
    orders = db.relationship('Order', backref='user', lazy='dynamic')
    # Отношение один-ко-многим с таблицей Cart
    cart = db.relationship('Cart', backref='user', lazy='dynamic', cascade='all, delete, delete-orphan')
    balance = db.Column(db.Float, default=0, index=True)

    # Отношение один-ко-многим с таблицей Cart

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None


class Status(db.Model):
    """Модель Статус заказа"""
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)


class Order(db.Model):
    """Модель Заказ"""
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_price = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))


class Cart(db.Model):
    """Модель Корзина"""
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))

    game = db.relationship('Game', backref='cart', lazy='joined', cascade='save-update, merge')

#
# def drop_tables():
#     with app.app_context():
#         db.drop_all()
#
#
