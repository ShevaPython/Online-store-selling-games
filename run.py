from app import app
from app.database import create_tables

# Создание таблиц перед запуском приложения
create_tables()

if __name__ == '__main__':
    app.run(debug=True)
