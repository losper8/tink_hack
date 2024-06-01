FROM python:3.9-slim

WORKDIR /opt/app-root/src/

COPY src/telegram_bot/requirements.txt /opt/app-root/src/telegram_bot/
RUN pip install --no-cache-dir -r /opt/app-root/src/telegram_bot/requirements.txt

ENV PYTHONPATH /opt/app-root/src
ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "--config", "/opt/app-root/src/telegram_bot/api/config/gunicorn.conf.py"]