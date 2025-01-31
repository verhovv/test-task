FROM python:3.13

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_PASSWORD=admin
ENV DJANGO_SUPERUSER_EMAIL=admin@example.com

COPY . .

RUN pip install -r requirements.txt

CMD python manage.py migrate && \
    python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME \
    --email $DJANGO_SUPERUSER_EMAIL --password $DJANGO_SUPERUSER_PASSW