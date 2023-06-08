from app_shop import app
from app_shop.models import create_tables,drop_tables

# drop_tables()
# # Создание таблиц перед запуском приложения
create_tables()

if __name__ == '__main__':
    app.run(debug=True)
