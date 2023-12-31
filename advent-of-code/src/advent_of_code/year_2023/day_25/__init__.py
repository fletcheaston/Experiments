from pathlib import Path

import networkx as nx
import pytest


def part_1(document: list[str]) -> int:
    graph = nx.Graph()

    # Add edges/nodes to the graph
    for line in document:
        start, rest = line.split(": ")

        for other in rest.split(" "):
            graph.add_edge(start, other)

    # Get minimum set of edges to cut from the graph to disconnect the graph
    cuts = nx.minimum_edge_cut(graph)

    # Remove those edges
    graph.remove_edges_from(cuts)

    # Count the size of each group in the graph
    total = 1

    for group in list(nx.connected_components(graph)):
        total *= len(group)

    return total


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example-1.txt", 54),
        ("input.txt", 543036),
    ],
)
def test_part_1(
    filename: str,
    output: int,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_1(file.read().splitlines()) == output
