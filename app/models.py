from app import db, app

class Developer(db.Model):
    __tablename__ = 'developer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    developer_site = db.Column(db.String(45), nullable=False)

    # Отношение один-ко-многим с таблицей Games
    games = db.relationship('Game', backref='game_all_developer', lazy=True)


class Publisher(db.Model):
    __tablename__ = 'publisher'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    publisher_site = db.Column(db.String(45), nullable=False)

    # Отношение один-ко-многим с таблицей Games
    games = db.relationship('Game', backref='game_all_publisher', lazy=True)


class Game(db.Model):
    __tablename__ = 'game'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    developer_id = db.Column(db.Integer, db.ForeignKey('developer.id'), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey('publisher.id'), nullable=False)
    photo = db.Column(db.String(200), nullable=True)
    # Отношение многие-к-одному с таблицей Developers
    developer = db.relationship('Developer', backref='developer_one', lazy=True)

    # Отношение многие-к-одному с таблицей Publishers
    publisher = db.relationship('Publisher', backref='publisher_one', lazy=True)


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)

    # Отношение многие-ко-многим с таблицей Games
    games = db.relationship('Games', secondary='games_genres', lazy='subquery',
                            backref=db.backref('genres', lazy=True))


class GamesGenres(db.Model):
    __tablename__ = 'games_genres'
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), primary_key=True)



class User(db.Model,):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    # Отношение один-ко-многим с таблицей Orders
    orders = db.relationship('Order', backref='client', lazy=True)


class Status(db.Model):
    __tablename__ = 'status'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)


class Order(db.Model):
    __tablename__ = 'order'
    id= db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'))

    # Отношение один-ко-многим с таблицей Cart
    cart = db.relationship('Cart', backref='order_card', lazy=True)


class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))

    # Обратная ссылка на заказ
    order = db.relationship('Orders', backref='cart_items')


def create_tables():
    with app.app_context():
        db.create_all()
