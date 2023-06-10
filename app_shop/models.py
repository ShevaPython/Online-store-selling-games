from flask_login import UserMixin
from app_shop import db, manager


# Ваш код моделей


class Developer(db.Model):
    __tablename__ = 'developer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    developer_site = db.Column(db.String(45), nullable=False)
    # Отношение один-ко-многим с таблицей Games
    games = db.relationship('Game', backref='developer', lazy=True)


class Publisher(db.Model):
    __tablename__ = 'publisher'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    publisher_site = db.Column(db.String(45), nullable=False)

    # Отношение один-ко-многим с таблицей Games
    games = db.relationship('Game', backref='publisher', lazy=True)


class GamesGenres(db.Model):
    __tablename__ = 'games_genres'
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), primary_key=True)


class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    developer_id = db.Column(db.Integer, db.ForeignKey('developer.id'), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'), nullable=False)
    photo = db.Column(db.String(200), nullable=True)
    # Отношение многие-ко-многим с моделью Genre
    genres = db.relationship('Genre', secondary='games_genres', lazy='subquery',
                             backref=db.backref('games', lazy=True))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    login = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean(), default=True)
    confirmed_at = db.Column(db.DateTime())
    # Отношение один-ко-многим с таблицей Orders
    orders = db.relationship('Order', backref='user', lazy=True)

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None


class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))


class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    # Обратная ссылка на заказ
    order = db.relationship('Order', backref='cart')


@manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


#
# def drop_tables():
#     with app.app_context():
#         db.drop_all()
#
#

