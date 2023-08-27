FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE DayPay.settings

RUN mkdir /app
WORKDIR /app

RUN pip install gunicorn

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD []
CMD ["gunicorn", "DayPay.wsgi:application", "--bind", "0.0.0.0:8000"]