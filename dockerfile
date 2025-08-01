FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir rich

ENV PYTHONPATH=/app

CMD ["python", "skibidi/entrypoint.py"]
