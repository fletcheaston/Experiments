from typing import Any, Iterator


def reduce_lfind(a: str, b: str, line: str) -> str:
    position_a = line.find(a)
    position_b = line.find(b)

    if position_a == -1:
        return b

    if position_b == -1:
        return a

    if position_a < position_b:
        return a

    return b


def reduce_rfind(a: str, b: str, line: str) -> str:
    position_a = line.rfind(a)
    position_b = line.rfind(b)

    if position_a == -1:
        return b

    if position_b == -1:
        return a

    if position_a > position_b:
        return a

    return b


def chunks(data: list[Any], size: int) -> Iterator[list[Any]]:
    """Yield successive chunks from data."""
    for i in range(0, len(data), size):
        yield data[i : i + size]
