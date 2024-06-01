FROM python:3.9-slim

WORKDIR /opt/app-root/src/

COPY src/embeddings/requirements.txt /opt/app-root/src/embeddings/

RUN pip install --no-cache-dir -r /opt/app-root/src/embeddings/requirements.txt

ENV PYTHONPATH /opt/app-root/src
ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "--config", "/opt/app-root/src/embeddings/api/config/gunicorn.conf.py"]