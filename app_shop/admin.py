from flask import redirect, url_for
from flask_admin.contrib.sqla import ModelView
from flask_admin import AdminIndexView, expose, Admin
from flask_login import current_user, login_required

from app_shop.models import Developer, Publisher, Game, Genre, db


class CustomAdminIndexView(AdminIndexView):
    @expose('/')
    @login_required  # Декоратор login_required требует аутентификации пользователя
    def index(self):
        # Проверяем, является ли текущий пользователь администратором
        if not current_user.is_admin:
            # Если пользователь не является администратором, перенаправляем его на другую страницу
            return redirect(url_for('index'))
        # Если пользователь является администратором, отображаем стандартный шаблон админ-панели
        return super(CustomAdminIndexView, self).index()


admin = Admin(index_view=CustomAdminIndexView())


class DeveloperModelView(ModelView):
    column_list = ('name', 'description', 'developer_site', 'games')


class PublisherModelView(ModelView):
    column_list = ('name', 'description', 'publisher_site', 'games')


class GameModelView(ModelView):
    column_list = ('name', 'price', 'genres', 'photo', 'twitch_stream', 'developer', 'publisher',)


class GenreModelView(ModelView):
    column_list = ('name', 'games')


# Регестрируем представления моделей в административной панели
admin.add_view(DeveloperModelView(Developer, db.session))
admin.add_view(PublisherModelView(Publisher, db.session))
admin.add_view(GameModelView(Game, db.session))
admin.add_view(GenreModelView(Genre, db.session))
