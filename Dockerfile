FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml ./
COPY requirements.lock ./
COPY requirements-build.lock ./
COPY config ./config
COPY ladder ./ladder
COPY gd_extreme_demon_ladder_generator ./gd_extreme_demon_ladder_generator
COPY manage.py ./

RUN pip install --no-cache-dir --only-binary=:all: \
        --require-hashes \
        --requirement requirements.lock \
        --requirement requirements-build.lock \
    && pip install --no-cache-dir --no-build-isolation --no-deps . \
    && addgroup --system django \
    && adduser --system --ingroup django django \
    && mkdir -p /app/data \
    && chown -R django:django /app

USER django

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2"]
