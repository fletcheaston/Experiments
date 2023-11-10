from fastapi import FastAPI
from models import Document
from sql import sync_db
from sqlalchemy import func
from sqlalchemy import select

app = FastAPI(root_path="/experiments/full-text-search")


def search(phrase: str) -> list[str]:
    session = sync_db()

    words = phrase.lower().split(" ")

    query = select(Document).limit(10)

    for word in words:
        query = query.where(func.lower(Document.definitions).contains(word))

    results = session.execute(query).scalars()

    return [result.word for result in results]
