FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ /app

RUN python manage.py collectstatic --noinput --settings=backend.settings.prod

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]
