FROM python:3.9-slim

WORKDIR /opt/app-root/src/

COPY src/rag_pipeline/requirements.txt /opt/app-root/src/rag_pipeline/

RUN pip install --no-cache-dir -r /opt/app-root/src/rag_pipeline/requirements.txt

ENV PYTHONPATH /opt/app-root/src
ENV PYTHONUNBUFFERED=1

CMD ["gunicorn", "--config", "/opt/app-root/src/rag_pipeline/api/config/gunicorn.conf.py"]