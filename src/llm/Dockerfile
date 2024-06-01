FROM python:3.9-slim

WORKDIR /opt/app-root/src/

COPY src/giga_chat/requirements.txt /opt/app-root/src/giga_chat/

RUN pip install --no-cache-dir -r /opt/app-root/src/giga_chat/requirements.txt

ENV PYTHONPATH /opt/app-root/src
ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "--config", "/opt/app-root/src/giga_chat/api/config/gunicorn.conf.py"]