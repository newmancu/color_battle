#!/bin/sh

echo "Connection to DB"

while ! nc -z ${SQL_HOST} ${SQL_PORT}; do
  sleep .2s
done

echo "Connected!"

python ./color_battle/manage.py makemigrations
python ./color_battle/manage.py makemigrations color_battle
python ./color_battle/manage.py migrate
python ./color_battle/manage.py migrate color_battle
python ./color_battle/manage.py base_configuration

exec "$@"