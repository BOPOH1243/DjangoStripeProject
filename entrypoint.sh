#!/bin/sh
# entrypoint.sh

# Применение миграций
python stripe_demo/manage.py migrate --noinput

# Создание суперпользователя
echo "from django.contrib.auth import get_user_model; User = get_user_model(); \
User.objects.create_superuser('admin', 'admin@example.com', 'admin') \
if not User.objects.filter(username='admin').exists() else None" | python stripe_demo/manage.py shell

# Запуск сервера
exec python stripe_demo/manage.py runserver 0.0.0.0:8000