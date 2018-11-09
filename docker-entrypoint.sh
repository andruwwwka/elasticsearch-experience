#!/bin/bash

elastic_host=$1
elastic_port=$2

postgres_host=$3
postgres_port=$4

# Ожидаем, пока elastic не будет запущен
while ! nc elastic_host elastic_port; do
  echo "Elasticsearch is unavailable - sleeping"
  sleep 1
done

# Ожидаем, пока postgres не будет запущен
while ! nc $postgres_host $postgres_port; do
  echo "Postgres is unavailable - sleeping"
  sleep 1
done

echo "Postgres is up - executing command"

# Накатываем миграции
echo "Apply database migrations"
python manage.py migrate

# Заполняем таблицы из фикстур
echo "Filling the tables"
python manage.py loaddata fixtures/data.json

# Запускаем сервер
echo "Starting server"
python manage.py runserver 0.0.0.0:8000