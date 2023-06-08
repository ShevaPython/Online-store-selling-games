from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DB_NAME, DB_HOST, DB_USER, DB_PASSWORD
from flask_login import LoginManager
from auth.auth import auth_bp

app = Flask(__name__,static_folder='static',template_folder='templates')
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = F"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '1bfe3c8bfc7bce5d5a9212fc319eea98'

# Регистрация Blueprint для авторизации
app.register_blueprint(auth_bp, url_prefix='/auth')

# Инициализация базы данных
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# После создания фактического объекта приложения вы можете настроить его для входа в систему с помощью
manager = LoginManager(app)

from app_shop import routes, models
