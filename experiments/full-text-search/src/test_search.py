import pytest
from main import search


@pytest.mark.parametrize(
    "word",
    [
        "the",
        "be",
        "to",
        "of",
        "and",
        "a",
        "in",
        "that",
        "have",
        "it",
    ],
)
def test_search_exact_word_match(word: str) -> None:
    results = search(word)

    assert len(results) > 0
    assert results[0] == word
