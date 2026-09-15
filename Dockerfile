FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml ./
COPY config ./config
COPY ladder ./ladder
COPY gd_extreme_demon_ladder_generator ./gd_extreme_demon_ladder_generator
COPY manage.py ./

RUN mkdir -p /app/data && pip install --no-cache-dir .

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2"]
