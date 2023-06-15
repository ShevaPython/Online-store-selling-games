from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import DB_NAME, DB_HOST, DB_USER, DB_PASSWORD, SECRET_KEY

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = F"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY
# Инициализация базы данных
db = SQLAlchemy(app)
# flask db migrate -m "Initial migration"
# Примените миграцию к базе данных: flask db upgrade
migrate = Migrate(app, db)
# После создания фактического объекта приложения вы можете настроить его для входа в систему с помощью
manager = LoginManager(app)

from auth.register import auth_bp
from basket.basket import card_bp
from app_shop.routes import *

# Регистрация Blueprint для авторизации
app.register_blueprint(auth_bp, url_prefix='/auth')
# Регистрация Blueprint для basket
app.register_blueprint(card_bp, url_prefix='/basket')


with app.app_context():
    db.create_all()
