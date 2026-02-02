from __future__ import annotations

import dataclasses
from typing import Any, Dict, List, Mapping, Sequence, Tuple

from agent_loom.ticket.frontmatter import normalize_list_value
from agent_loom.ticket.constants import NON_TERMINAL_STATUSES
from agent_loom.ticket.models import Ticket


def has_cycle(graph: Mapping[str, Sequence[str]]) -> bool:
    visited: set[str] = set()
    stack: set[str] = set()

    def visit(node: str) -> bool:
        if node in stack:
            return True
        if node in visited:
            return False
        visited.add(node)
        stack.add(node)
        for n2 in graph.get(node, []) or []:
            if visit(str(n2)):
                return True
        stack.remove(node)
        return False

    return any(visit(n) for n in graph.keys())


def simple_cycles(graph: Mapping[str, Sequence[str]]) -> List[List[str]]:
    cycles: set[Tuple[str, ...]] = set()

    def dfs(start: str, cur: str, path: List[str], on_path: set[str]) -> None:
        for nxt in graph.get(cur, []) or []:
            nxt = str(nxt)
            if nxt == start:
                body = path
                if body:
                    m = min(range(len(body)), key=lambda i: body[i])
                    canon = tuple(body[m:] + body[:m])
                    cycles.add(canon)
                continue
            if nxt in on_path:
                continue
            on_path.add(nxt)
            dfs(start, nxt, path + [nxt], on_path)
            on_path.remove(nxt)

    for node in sorted(graph.keys()):
        dfs(node, node, [node], {node})

    return [list(c) for c in sorted(cycles)]


def predecessors(graph: Mapping[str, Sequence[str]]) -> Dict[str, List[str]]:
    pred: Dict[str, List[str]] = {}
    for a, ds in graph.items():
        for d in ds or []:
            d = str(d)
            pred.setdefault(d, []).append(str(a))
    for k in list(pred.keys()):
        pred[k] = sorted(set(pred[k]))
    return pred


@dataclasses.dataclass
class GraphIndex:
    tickets: Dict[str, Ticket]
    deps: Dict[str, List[str]]
    parent: Dict[str, List[str]]
    links: Dict[str, List[str]]
    missing: List[str]

    def ticket(self, tid: str) -> Ticket | None:
        return self.tickets.get(tid)


def build_index(store) -> GraphIndex:
    tickets: Dict[str, Ticket] = {}
    missing: List[str] = []

    for p in store.iter_paths():
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue
        from agent_loom.ticket.frontmatter import split_frontmatter

        fm, body = split_frontmatter(text)
        tid = str(fm.get("id") or p.stem)
        fm["id"] = tid
        tickets[tid] = Ticket(path=p, fm=fm, body=body)

    deps: Dict[str, List[str]] = {tid: [] for tid in tickets}
    parent: Dict[str, List[str]] = {tid: [] for tid in tickets}
    links: Dict[str, List[str]] = {tid: [] for tid in tickets}

    for tid, t in tickets.items():
        for d in normalize_list_value(t.fm.get("deps")):
            deps.setdefault(tid, []).append(d)
            if d not in tickets:
                missing.append(d)
        for link_id in normalize_list_value(t.fm.get("links")):
            links.setdefault(tid, []).append(link_id)
            if link_id not in tickets:
                missing.append(link_id)
        p = str(t.fm.get("parent") or "").strip()
        if p:
            parent.setdefault(p, []).append(tid)
            if p not in tickets:
                missing.append(p)

    for a, bs in list(links.items()):
        for b in bs:
            links.setdefault(b, [])
            if a not in links[b]:
                links[b].append(a)

    for m in (deps, parent, links):
        for k in list(m.keys()):
            m[k] = sorted(set([x for x in m[k] if x]))

    return GraphIndex(
        tickets=tickets,
        deps=deps,
        parent=parent,
        links=links,
        missing=sorted(set(missing)),
    )


def blockers_for(tid: str, idx: GraphIndex) -> List[str]:
    t = idx.ticket(tid)
    if not t:
        return []
    blockers: List[str] = []
    for d in idx.deps.get(tid, []):
        dt = idx.ticket(d)
        if not dt:
            blockers.append(d)
        elif dt.status != "closed":
            blockers.append(d)
    return sorted(set(blockers))


def is_ready(tid: str, idx: GraphIndex) -> bool:
    t = idx.ticket(tid)
    if not t:
        return False
    # Tickets can be "ready" due to deps even if their status is still open.
    # Treat explicit "blocked" as not-ready, even if deps are empty.
    if t.status == "blocked":
        return False
    if t.status not in NON_TERMINAL_STATUSES:
        return False
    return len(blockers_for(tid, idx)) == 0


def is_blocked(tid: str, idx: GraphIndex) -> bool:
    t = idx.ticket(tid)
    if not t:
        return False
    # Explicitly blocked tickets are always considered blocked.
    if t.status == "blocked":
        return True
    if t.status not in NON_TERMINAL_STATUSES:
        return False
    return len(blockers_for(tid, idx)) > 0


def closure_from(
    root: str,
    idx: GraphIndex,
    *,
    include_parents: bool = False,
    include_children: bool = True,
) -> Tuple[set[str], set[Tuple[str, str, str]]]:
    nodes: set[str] = set()
    edges: set[Tuple[str, str, str]] = set()

    def add_node(x: str) -> None:
        nodes.add(x)

    def add_edge(a: str, b: str, kind: str) -> None:
        edges.add((a, b, kind))

    add_node(root)

    q = [root]
    seen_pc = set(q)
    while q:
        cur = q.pop(0)
        if include_children:
            for child in idx.parent.get(cur, []):
                add_node(child)
                add_edge(cur, child, "parent")
                if child not in seen_pc:
                    seen_pc.add(child)
                    q.append(child)
        if include_parents:
            for parent in [p for p, ch in idx.parent.items() if cur in ch]:
                add_node(parent)
                add_edge(parent, cur, "parent")
                if parent not in seen_pc:
                    seen_pc.add(parent)
                    q.append(parent)

    dep_q = list(nodes)
    seen_dep = set(dep_q)
    while dep_q:
        cur = dep_q.pop(0)
        for dep in idx.deps.get(cur, []):
            add_node(dep)
            add_edge(cur, dep, "dep")
            if dep not in seen_dep:
                seen_dep.add(dep)
                dep_q.append(dep)

    for a in list(nodes):
        for b in idx.links.get(a, []):
            if b in nodes:
                add_edge(a, b, "link")

    return nodes, edges


def topo_layers_by_block_depth(
    idx: GraphIndex, root: str, nodes: set[str]
) -> Dict[str, int]:
    depths: Dict[str, int] = {str(n): 0 for n in nodes}
    if root not in nodes:
        return depths

    q: List[str] = [root]
    seen = {root}
    while q:
        cur = q.pop(0)
        cur_d = depths.get(cur, 0)
        for dep in idx.deps.get(cur, []):
            if dep not in nodes:
                continue
            if dep not in depths or cur_d + 1 > depths[dep]:
                depths[dep] = cur_d + 1
            if dep not in seen:
                seen.add(dep)
                q.append(dep)

    return depths


def compute_health(nodes: set[str], idx: GraphIndex) -> Dict[str, Any]:
    counts = {
        "open": 0,
        "ready": 0,
        "in_progress": 0,
        "blocked": 0,
        "review": 0,
        "closed": 0,
        "missing": 0,
    }
    blocked = 0
    ready = 0
    for n in sorted(nodes):
        t = idx.ticket(n)
        if not t:
            counts["missing"] += 1
            continue
        counts[t.status] = counts.get(t.status, 0) + 1
        if is_ready(n, idx):
            ready += 1
        if is_blocked(n, idx):
            blocked += 1

    dependents: Dict[str, List[str]] = {}
    for a, ds in idx.deps.items():
        for d in ds:
            dependents.setdefault(d, []).append(a)

    def descendants(start: str) -> set[str]:
        out: set[str] = set()
        q = list(dependents.get(start, []))
        while q:
            cur = q.pop(0)
            if cur in out:
                continue
            out.add(cur)
            q.extend(dependents.get(cur, []))
        return out

    block_counts: List[Tuple[int, str]] = []
    for n in nodes:
        t = idx.ticket(n)
        if not t or t.status == "closed":
            continue
        ds = descendants(n) & set(nodes)
        score = sum(
            1 for x in ds if (tx := idx.ticket(x)) is not None and tx.status != "closed"
        )
        block_counts.append((score, n))
    block_counts.sort(reverse=True)

    return {
        "counts": counts,
        "ready": ready,
        "blocked": blocked,
        "bottlenecks": [
            {
                "id": n,
                "blocks": s,
                "title": (tn.title if (tn := idx.ticket(n)) is not None else ""),
            }
            for s, n in block_counts[:10]
            if s > 0
        ],
    }


__all__ = [
    "GraphIndex",
    "blockers_for",
    "build_index",
    "compute_health",
    "closure_from",
    "has_cycle",
    "is_blocked",
    "is_ready",
    "predecessors",
    "simple_cycles",
    "topo_layers_by_block_depth",
]
