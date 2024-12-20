#!/bin/sh

#cd /code/
python /code/manage.py migrate
#python manage.py makemigrations
#python /code/manage.py collectstatic #--no-input

python /code/manage.py runserver 0.0.0.0:8000

#cp -r /code/mimicINTapp/static/ /

gunicorn mimicINT.wsgi:application --bind 0.0.0.0:8000




# Prepare log files and start outputting logs to stdout
mkdir -p /code/logs
touch /code/logs/gunicorn.log
touch /code/logs/gunicorn-access.log
tail -n 0 -f /code/logs/gunicorn*.log &

export DJANGO_SETTINGS_MODULE=mimicINT.settings

exec gunicorn mimicINT.wsgi:application \
    --name mimicINT \
    --bind 0.0.0.0:8000 \
    --workers 5 \
    --log-level=info \
    --log-file=/code/logs/gunicorn.log \
    --access-logfile=/code/logs/gunicorn-access.log \
"$@"
