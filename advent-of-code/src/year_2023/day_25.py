import networkx as nx
from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 25: Title"])


DOCUMENT_EXAMPLE = []


@router.post("/part-1")
async def year_2023_day_25_part_1(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
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
