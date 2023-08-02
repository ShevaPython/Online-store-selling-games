FROM python:3.8-alpine

# Устанавливаем системные зависимости для сборки mysqlclient и Git
RUN apk add --no-cache mariadb-dev build-base git

WORKDIR /app
COPY .env /app
COPY . /app

# Установка пакета, который содержит mysql_config
RUN apk add --no-cache mariadb-connector-c-dev

# Установка Gunicorn
RUN pip install gunicorn

# Установка зависимостей вашего приложения
RUN pip install -r requirements.txt

# Открываем порт 8000, на котором будет работать Gunicorn
EXPOSE 8000

# Запуск Gunicorn в качестве сервера
CMD ["gunicorn", "-b", "0.0.0.0:8000", "wsgi:app"]



