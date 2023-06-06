from app import db,app


class Developers(db.Model):
    __tablename__ = 'developers'
    iddevelopers = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    developer_site = db.Column(db.String(45), nullable=False)

    # Отношение один-ко-многим с таблицей Games
    games = db.relationship('Games', backref='developer', lazy=True)


class Publishers(db.Model):
    __tablename__ = 'publishers'
    idpublishers = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    publisher_site = db.Column(db.String(45), nullable=False)

    # Отношение один-ко-многим с таблицей Games
    games = db.relationship('Games', backref='publisher', lazy=True)


class Games(db.Model):
    __tablename__ = 'games'
    idgames = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    developers_iddevelopers = db.Column(db.Integer, db.ForeignKey('developers.iddevelopers'), nullable=False)
    publishers_idpublishers = db.Column(db.Integer, db.ForeignKey('publishers.idpublishers'), nullable=False)
    photo = db.Column(db.String(200),nullable=True)
    # Отношение многие-к-одному с таблицей Developers
    developer = db.relationship('Developers', backref='games', lazy=True)

    # Отношение многие-к-одному с таблицей Publishers
    publisher = db.relationship('Publishers', backref='games', lazy=True)


class Genres(db.Model):
    __tablename__ = 'gernes'
    idgerne = db.Column(db.Integer, primary_key=True)
    gerne_name = db.Column(db.String(45), nullable=False)

    # Отношение многие-ко-многим с таблицей Games
    games = db.relationship('Games', secondary='games_gernes', lazy='subquery',
                            backref=db.backref('gernes', lazy=True))


class GamesGenres(db.Model):
    __tablename__ = 'games_gernes'
    games_idgames = db.Column(db.Integer, db.ForeignKey('games.idgames'), primary_key=True)
    gerne_idgerne = db.Column(db.Integer, db.ForeignKey('gernes.idgerne'), primary_key=True)


class Clients(db.Model):
    __tablename__ = 'clients'
    idclients = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    surname = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    date_of_registration = db.Column(db.Date, nullable=False)
    online_wallet = db.Column(db.Float)

    # Отношение один-ко-многим с таблицей Orders
    orders = db.relationship('Orders', backref='client', lazy=True)


class Status(db.Model):
    __tablename__ = 'status'
    idstatus = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)


class Orders(db.Model):
    __tablename__ = 'orders'
    idorders = db.Column(db.Integer, primary_key=True)
    order_date = db.Column(db.Date, nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    clients_idclients = db.Column(db.Integer, db.ForeignKey('clients.idclients'))
    status_idstatus = db.Column(db.Integer, db.ForeignKey('status.idstatus'))

    # Отношение один-ко-многим с таблицей Cart
    cart = db.relationship('Cart', backref='order', lazy=True)


class Cart(db.Model):
    __tablename__ = 'cart'
    idcart = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    games_idgames = db.Column(db.Integer, db.ForeignKey('games.idgames'))
    orders_idorders = db.Column(db.Integer, db.ForeignKey('orders.idorders'))

    # Обратная ссылка на заказ
    order = db.relationship('Orders', backref='cart_items')


def create_tables():
    with app.app_context():
        db.create_all()
