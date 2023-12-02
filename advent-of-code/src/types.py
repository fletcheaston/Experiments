import io
from typing import Annotated

from fastapi import Depends, UploadFile


def lines(document: UploadFile) -> list[str]:
    all_lines: list[str] = []

    with document.file as file:
        for line in io.TextIOWrapper(file, encoding="utf-8"):
            all_lines.append(line.strip())

    return all_lines


Lines = Annotated[list[str], Depends(lines)]
