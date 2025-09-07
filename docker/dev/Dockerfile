FROM python:3.11-slim

WORKDIR /app

COPY blog/requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY blog/ /app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
