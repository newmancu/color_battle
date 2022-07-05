#!/bin/sh

echo "Connection to DB"

while ! nc -z ${SQL_HOST} ${SQL_PORT}; do
  sleep .2s
done

echo "Connected!"

python ./color_battle/manage.py makemigrations
python ./color_battle/manage.py makemigrations back_api
python ./color_battle/manage.py migrate
python ./color_battle/manage.py migrate back_api
python ./color_battle/manage.py collectstatic --noinput
python ./color_battle/manage.py base_configuration

exec "$@"