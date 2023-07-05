from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail

from .models import db, User
from .helpers import inject_cart_count, inject_genres
from config import DB_NAME, DB_HOST, DB_USER, DB_PASSWORD, SECRET_KEY,GMAIL_PASSWORD



# Create the redis object
redis = FlaskRedis()
# Create the manager object
manager = LoginManager()
# Create the toolbar object
toolbar = DebugToolbarExtension()

# create object mail
mail = Mail()


def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Enable query recording
    app.config['SQLALCHEMY_RECORD_QUERIES'] = True

    app.config['SECRET_KEY'] = SECRET_KEY

    # redis
    app.config['REDIS_URL'] = 'redis://localhost:6379/0'
    redis.init_app(app)

    # Настройка расширения Flask-DebugToolbar
    app.config['DEBUG_TB_ENABLED'] = True  # Включение Debug Toolbar
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False  # Отключение перехвата перенаправлений
    toolbar.init_app(app)


    #Настройка расширения Mail
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'shevadotka@gmail.com'
    app.config['MAIL_PASSWORD'] = GMAIL_PASSWORD
    app.config['MAIL_DEFAULT_SENDER'] = 'shevadotka@gmail.com'
    mail.init_app(app)

    # Регистрация контекстных процессоров
    app.context_processor(inject_cart_count)
    app.context_processor(inject_genres)

    # Инициализация базы данных
    db.init_app(app)

    manager.init_app(app)
    # manager.login_view = 'auth.login_page'


    # flask db migrate -m "Initial migration"
    # Примените миграцию к базе данных: flask db upgrade
    migrate = Migrate(app, db)



    from auth.register import auth_bp
    # Регистрация Blueprint для авторизации
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from basket.basket import cart_bp
    # Регистрация Blueprint для basket
    app.register_blueprint(cart_bp, url_prefix='/basket')

    # Регистрация Blueprint для blog
    from .routes import bp as dp_blog
    app.register_blueprint(dp_blog)
    app.add_url_rule('/', endpoint='index')

    return app
