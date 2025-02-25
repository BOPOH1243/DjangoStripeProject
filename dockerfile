# Используем официальный Python образ
FROM python:3.12-slim

# Устанавливаем системные зависимости (если нужно)
RUN apt-get update && apt-get install -y build-essential libpq-dev --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y wait-for-it

# Создаём рабочую директорию
WORKDIR /code

# Копируем файлы зависимостей
COPY requirements.txt /code/

# Устанавливаем Python зависимости
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /code/

# Собираем статику, выполняем миграции или другие подготовительные команды
# RUN python manage.py collectstatic --noinput
# RUN python manage.py migrate

# По умолчанию запуск Gunicorn (см. docker-compose.yml, command)
