FROM python:3.12

WORKDIR /app

COPY pyproject.toml ./

RUN pip install .

COPY . .

RUN mkdocs build

ENTRYPOINT uvicorn app:app --proxy-headers --forwarded-allow-ips "*" --host 0.0.0.0 --port 8080
