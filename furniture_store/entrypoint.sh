python furnitore_store/manage.py migrate

python furnitore_store/manage.py collectstatic --noinput

exec gunicorn furniture_store.wsgi:application --bind 127.0.0.1:8000 --workers 3