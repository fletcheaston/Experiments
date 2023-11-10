import json
import uuid
from pathlib import Path
from typing import Any

from main import search
from models import Document
from sql import sync_db
from sqlalchemy.dialects.postgresql import insert
from typer import Typer

cli = Typer()


@cli.command()
def search_dictionary(phrase: str) -> None:
    """Search dictionary for a particular phrase."""
    results = search(phrase)

    for result in results:
        print(result)


@cli.command()
def import_dictionary(file: Path) -> None:
    """Import a JSON file as a dictionary."""

    total_rows = 0
    bulk_add = 1_000
    session = sync_db()

    def upsert(rows: list[dict[str, Any]]) -> None:
        query = insert(Document).values(rows)

        session.execute(
            query.on_conflict_do_update(
                index_elements=["word"],
                set_={
                    "definitions": query.excluded.definitions,
                },
            )
        )

        session.commit()

    with open(file) as json_file:
        data = json.load(json_file)

        rows_to_upsert: list[dict[str, Any]] = []

        for key, value in data.items():
            rows_to_upsert.append(
                {
                    "id": uuid.uuid4(),
                    "word": key,
                    "definitions": value,
                }
            )

            if len(rows_to_upsert) >= bulk_add:
                upsert(rows_to_upsert)

                total_rows += bulk_add
                print(f"Rows: {total_rows}")

                rows_to_upsert = []

        # Upsert any stragglers
        upsert(rows_to_upsert)


if __name__ == "__main__":
    cli()
