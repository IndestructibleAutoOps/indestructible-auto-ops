from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DAG:
    nodes: list[dict[str, Any]]

    @staticmethod
    def from_nodes(nodes: list[dict[str, Any]]) -> DAG:
        return DAG(nodes=nodes)

    def ids(self) -> list[str]:
        return [n["id"] for n in self.nodes]

    def deps(self, node_id: str) -> list[str]:
        for n in self.nodes:
            if n["id"] == node_id:
                return list(n.get("deps", []))
        return []


def dag_is_acyclic(dag: DAG) -> bool:
    ids = set(dag.ids())
    graph: dict[str, list[str]] = {i: [] for i in ids}
    indeg: dict[str, int] = {i: 0 for i in ids}
    for i in ids:
        deps = [d for d in dag.deps(i) if d in ids]
        for d in deps:
            graph[d].append(i)
            indeg[i] += 1
    q = [i for i in ids if indeg[i] == 0]
    seen = 0
    while q:
        cur = q.pop()
        seen += 1
        for nxt in graph[cur]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                q.append(nxt)
    return seen == len(ids)


def topological_sort(dag: DAG) -> list[str] | None:
    """Return a topological ordering of DAG node IDs, or None if the DAG has a cycle.
    
    Uses Kahn's algorithm to compute the topological order. If the DAG contains
    a cycle, returns None instead of a partial ordering.
    
    Returns:
        List of node IDs in topological order, or None if cyclic.
    """
    ids = set(dag.ids())
    graph: dict[str, list[str]] = {i: [] for i in ids}
    indeg: dict[str, int] = {i: 0 for i in ids}
    
    # Build adjacency list and compute in-degrees
    for i in ids:
        deps = [d for d in dag.deps(i) if d in ids]
        for d in deps:
            graph[d].append(i)
            indeg[i] += 1
    
    # Start with nodes that have no dependencies
    q = [i for i in ids if indeg[i] == 0]
    result = []
    
    while q:
        # Process nodes in a stable order for deterministic results
        q.sort()
        cur = q.pop(0)
        result.append(cur)
        
        for nxt in graph[cur]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                q.append(nxt)
    
    # If we processed all nodes, return the ordering; otherwise there's a cycle
    return result if len(result) == len(ids) else None
