FROM python:3.12

WORKDIR /app

RUN pip install poetry

COPY poetry.toml ./
COPY pyproject.toml ./
COPY poetry.lock ./
COPY Makefile ./

RUN make setup

COPY . .

RUN make build

ENTRYPOINT poetry run uvicorn app:app --proxy-headers --forwarded-allow-ips "*" --host 0.0.0.0 --port 8080
