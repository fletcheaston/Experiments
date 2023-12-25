import networkx as nx
from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day N: Title"])


DOCUMENT_EXAMPLE = []


@router.post("/part-1")
async def year_2023_day_25_part_1(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    connections: dict[str, set[str]] = {}

    for line in document:
        start, rest = line.split(": ")

        if start not in connections:
            connections[start] = set()

        for other in rest.split(" "):
            if other not in connections:
                connections[other] = set()

            connections[start].add(other)
            connections[other].add(start)

    graph = nx.Graph()

    for start, others in connections.items():
        for other in others:
            graph.add_edge(start, other)

    cuts = nx.minimum_edge_cut(graph)

    graph.remove_edges_from(cuts)

    total = 1

    for group in list(nx.connected_components(graph)):
        total *= len(group)

    return total


@router.post("/part-2")
async def year_2023_day_25_part_2(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    total = 0

    for line in document:
        pass

    return total
