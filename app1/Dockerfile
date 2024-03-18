FROM python:3.10-slim

WORKDIR /appdir

COPY . /appdir/

RUN pip install -r req.txt

CMD python manage.py makemigrations \
    && python manage.py migrate \
    && python manage.py loaddata cats.json prod.json  \
    && python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='root').exists() or User.objects.create_superuser('root', 'root@example.com', 'root')" \
    && python manage.py collectstatic --noinput \
    && gunicorn app.wsgi:application --bind 0.0.0.0:8000