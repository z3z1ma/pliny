from datetime import date

from loom_mill.parser import parse_records


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def by_id(graph, record_id):
    return next(record for record in graph.records if record.metadata.id == record_id)


def test_parse_records_extracts_metadata_headings_references_and_labeled_ids(tmp_path):
    loom = tmp_path / ".loom"
    write(
        loom / "tickets" / "20260525-example.md",
        """# Example Ticket

ID: ticket:20260525-example
Type: Ticket
Status: open
Created: 2026-05-25
Updated: 2026-05-26
Risk: low - fixture
Priority: high - demo
Depends On: ticket:20260525-prereq, spec:loom-mill-factory-floor-mvp

## Summary

This cites `plan:20260525-factory-floor-mvp` and evidence:20260525-parser-check.

## Acceptance

- ACC-001: Covers REQ-002 and SCN-001.

### Detail

Finding reference FIND-004 and question OQ-005.
""",
    )
    write(
        loom / "specs" / "example.md",
        """# Example Spec

ID: spec:example
Type: Spec
Status: draft
Created: 2026-05-25
Updated: 2026-05-25

## Requirements

- REQ-001: Link to ticket:20260525-example and audit:20260525-parser-audit.

### Scenario

- SCN-001: Mentions knowledge:parser-procedure and decision:0002.
""",
    )

    graph = parse_records(loom)

    assert len(graph.records) == 2
    ticket = by_id(graph, "ticket:20260525-example")
    assert ticket.path == "tickets/20260525-example.md"
    assert ticket.surface == "tickets"
    assert ticket.metadata.type == "Ticket"
    assert ticket.metadata.status == "open"
    assert ticket.metadata.created == date(2026, 5, 25)
    assert ticket.metadata.updated == date(2026, 5, 26)
    assert ticket.metadata.risk == "low - fixture"
    assert ticket.metadata.priority == "high - demo"
    assert ticket.metadata.depends_on == (
        "ticket:20260525-prereq",
        "spec:loom-mill-factory-floor-mvp",
    )
    assert ticket.headings == ((1, "Example Ticket"), (2, "Summary"), (2, "Acceptance"), (3, "Detail"))
    assert ticket.references == (
        "ticket:20260525-example",
        "ticket:20260525-prereq",
        "spec:loom-mill-factory-floor-mvp",
        "plan:20260525-factory-floor-mvp",
        "evidence:20260525-parser-check",
    )
    assert ticket.labeled_ids == ("ACC-001", "REQ-002", "SCN-001", "FIND-004", "OQ-005")

    spec = by_id(graph, "spec:example")
    assert spec.references == (
        "spec:example",
        "ticket:20260525-example",
        "audit:20260525-parser-audit",
        "knowledge:parser-procedure",
        "decision:0002",
    )
    assert spec.labeled_ids == ("REQ-001", "SCN-001")


def test_parse_records_handles_edge_cases_without_crashing(tmp_path):
    records = tmp_path / "records"
    write(records / "empty.md", "")
    write(
        records / "non_loom.md",
        """# Plain Markdown

This is documentation, not a Loom record.

## Section

Malformed ACC-1 does not count, but ACC-001 does.
""",
    )
    write(
        records / "malformed.md",
        """# Malformed

ID ticket:20260525-missing-colon
Type: Ticket
Created: not-a-date
Updated: 2026-05-25
Depends On: ticket:not-a-valid-ticket, plan:20260525-valid-plan

## Body

References constitution:main, roadmap:loom-mill, principle:single-piece-flow, and research:20260524-topic.
""",
    )

    graph = parse_records(records)

    assert len(graph.records) == 3
    plain = next(record for record in graph.records if record.path == "non_loom.md")
    assert plain.metadata.id is None
    assert plain.headings == ((1, "Plain Markdown"), (2, "Section"))
    assert plain.references == ()
    assert plain.labeled_ids == ("ACC-001",)

    malformed = next(record for record in graph.records if record.path == "malformed.md")
    assert malformed.metadata.id is None
    assert malformed.metadata.type == "Ticket"
    assert malformed.metadata.created is None
    assert malformed.metadata.updated == date(2026, 5, 25)
    assert malformed.metadata.depends_on == ("plan:20260525-valid-plan",)
    assert malformed.references == (
        "ticket:20260525-missing-colon",
        "plan:20260525-valid-plan",
        "constitution:main",
        "roadmap:loom-mill",
        "principle:single-piece-flow",
        "research:20260524-topic",
    )
