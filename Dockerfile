FROM python:3.8.1-slim-buster

RUN useradd stats

EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    PORT=8000

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libmariadbclient-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    locales \
 && rm -rf /var/lib/apt/lists/*

# ENV LANG en_US.UTF-8
# ENV LC_ALL en_US.UTF-8

# RUN export LC_ALL=C

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
RUN pip install "gunicorn==20.0.4"


COPY . /app/
WORKDIR /app/
RUN chown -R stats /app


USER stats

RUN chmod +x run.sh

RUN python manage.py collectstatic --noinput --clear
# RUN python manage.py migrate --noinput
# RUN python manage.py import_rushing_stats
# CMD set -xe; python manage.py migrate --noinput; gunicorn stats.wsgi:application
CMD set -xe; gunicorn stats.wsgi:application