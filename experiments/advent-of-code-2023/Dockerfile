FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install .

RUN mkdocs build

ENTRYPOINT uvicorn app:app --proxy-headers --forwarded-allow-ips "*" --host 0.0.0.0 --port 8080
