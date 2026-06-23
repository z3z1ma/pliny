from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


SCENARIO_TARGETS = {
    "SCN-001": ("S001", "S007"),
    "SCN-002": ("S001", "S007"),
    "SCN-003": ("S001", "S002", "S007"),
    "SCN-004": ("S002",),
    "SCN-005": ("S002", "S005"),
    "SCN-006": ("S003",),
    "SCN-007": ("S003", "S006"),
    "SCN-008": ("S004",),
    "SCN-009": ("S004", "S006"),
    "SCN-010": ("S005", "S007"),
    "SCN-011": ("S005",),
    "SCN-012": ("S002", "S006"),
    "SCN-013": ("S008",),
    "SCN-014": ("S008",),
    "SCN-015": ("S008", "S006"),
}
SCENARIO_SUPPORT = {
    scenario_id: {
        "status": "partial" if scenario_id in {"SCN-007", "SCN-013", "SCN-014", "SCN-015"} else "supported",
        "reason": (
            "Offline fixtures approximate behavior from saved transcripts and file outputs; "
            "live harness identity, repeated model variance, or human verdict quality still needs manual review."
            if scenario_id in {"SCN-007", "SCN-013", "SCN-014", "SCN-015"}
            else ""
        ),
    }
    for scenario_id in SCENARIO_TARGETS
}
SCORE_SUPPORT = {
    "S001": {
        "status": "supported",
        "reason": "First-pass checks inspect transcript text, tool use, and file writes.",
    },
    "S002": {
        "status": "supported",
        "reason": "First-pass checks inspect saved .10x record paths and content.",
    },
    "S003": {
        "status": "supported",
        "reason": "First-pass checks inspect ticket shape, boundaries, references, and implementation writes.",
    },
    "S004": {
        "status": "supported",
        "reason": "First-pass checks inspect command output, evidence records, limits, and overclaims.",
    },
    "S005": {
        "status": "supported",
        "reason": "First-pass checks inspect dependency, abstraction, locality, and safety-rail signals.",
    },
    "S006": {
        "status": "supported",
        "reason": "First-pass checks inspect closure text, ticket/evidence/review paths, and follow-up handling.",
    },
    "S007": {
        "status": "partial",
        "reason": "Human shaping quality needs human review; offline output is only a transcript heuristic.",
    },
    "S008": {
        "status": "partial",
        "reason": "Research method quality needs manual inspection and repeated runs; offline output is only a record-shape heuristic.",
    },
    "S009": {
        "status": "unsupported",
        "reason": "Cost efficiency needs baseline-normalized cost telemetry, calibrated core quality, and cost policy.",
    },
}
ACTIVE_FLOORS = {
    "S001": 80,
    "S002": 80,
    "S003": 75,
    "S004": 80,
    "S005": 75,
    "S006": 80,
    "S008": 85,
}
TRUST_LEVEL = 1


def score_fixture(path: str | Path) -> dict[str, Any]:
    fixture_path = Path(path)
    fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
    scenario_id = fixture.get("scenario_id")
    if scenario_id not in SCENARIO_TARGETS:
        raise ValueError(f"unsupported offline scoring scenario: {scenario_id}")

    scores: dict[str, Any] = {}
    floor_triggers: list[dict[str, Any]] = []
    for score_id in SCENARIO_TARGETS[scenario_id]:
        result = _score_one(score_id, scenario_id, fixture)
        triggers = result.pop("floor_triggers")
        if score_id in ACTIVE_FLOORS and result["value"] < ACTIVE_FLOORS[score_id]:
            triggers.append(
                {
                    "score_id": score_id,
                    "condition": f"{score_id} below active floor {ACTIVE_FLOORS[score_id]}",
                    "cap": None,
                    "effect": "non-promotable without manual inspection",
                    "evidence_refs": result["evidence_refs"],
                }
            )
        result["floor_triggered"] = bool(triggers)
        result["floor_triggers"] = triggers
        scores[score_id] = result
        floor_triggers.extend(triggers)

    raw_refs = _string_list(fixture.get("raw_artifact_refs"))
    if str(fixture_path) not in raw_refs:
        raw_refs.append(str(fixture_path))
    scorer_limits = _scorer_limits(fixture)
    for score in scores.values():
        score["limits"] = scorer_limits

    return {
        "experiment_id": fixture.get("experiment_id"),
        "scenario_id": scenario_id,
        "variant_id": fixture.get("variant_id"),
        "rep": fixture.get("rep"),
        "model": fixture.get("model"),
        "harness": fixture.get("harness"),
        "instruction_digest": fixture.get("instruction_digest"),
        "fixture_digest": "sha256:" + _sha256(fixture_path),
        "scores": scores,
        "cost": {
            "wall_seconds": float(fixture.get("wall_seconds", 0)),
            "input_tokens": fixture.get("input_tokens"),
            "output_tokens": fixture.get("output_tokens"),
            "tool_calls": len(_list(fixture.get("tool_invocations"))),
            "estimated_usd": fixture.get("estimated_usd"),
            "human_inspection_seconds": None,
            "resident_context_tokens": fixture.get("resident_context_tokens"),
        },
        "limits": scorer_limits,
        "scorer": {
            "id": "offline-coverage-v1",
            "trust_level": TRUST_LEVEL,
            "inputs": [
                "saved transcript",
                "saved tool invocations",
                "saved file outputs",
                "saved command outputs",
            ],
            "outputs": [
                "numeric score",
                "confidence",
                "rationale",
                "evidence_refs",
                "unsupported_assumptions",
                "floor_triggers",
            ],
            "known_false_positives": [
                "Keyword matches may reward policy language that was not applied.",
                "Fixture file paths may look coherent while omitted surrounding records would fail review.",
            ],
            "known_false_negatives": [
                "Terse correct refusals may lack the phrases this tracer recognizes.",
                "Equivalent evidence wording may score low until manually inspected.",
            ],
            "confidence": "low",
            "manual_inspection_required": True,
            "manual_inspection_requirement": (
                "Manual inspection is required before using Trust Level 1 "
                "offline tracer scores for promotion or durable verdicts."
            ),
            "limits": scorer_limits,
        },
        "manual_inspection": {
            "status": "required-not-done",
            "artifact_refs": raw_refs,
            "limits": [
                "No human reviewer inspected this score artifact during scoring."
            ],
        },
        "floor_triggers": floor_triggers,
        "raw_artifact_refs": raw_refs,
    }


def validate_score_artifact(artifact: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = (
        "experiment_id",
        "scenario_id",
        "variant_id",
        "rep",
        "model",
        "harness",
        "instruction_digest",
        "fixture_digest",
        "scores",
        "cost",
        "limits",
        "scorer",
    )
    for field in required:
        if field not in artifact:
            errors.append(f"artifact: missing {field}")

    if not _matches(artifact.get("experiment_id"), r"^EXP-\d{8}-\d{3}-[a-z0-9]+(?:-[a-z0-9]+)*$"):
        errors.append("artifact: invalid experiment_id")
    if not _matches(artifact.get("scenario_id"), r"^SCN-\d{3}(?:-[a-z0-9]+)*$"):
        errors.append("artifact: invalid scenario_id")
    for field in ("variant_id", "model", "harness", "instruction_digest", "fixture_digest"):
        if not _non_empty_string(artifact.get(field)):
            errors.append(f"artifact: {field} must be a non-empty string")
    if not isinstance(artifact.get("rep"), int) or artifact["rep"] < 0:
        errors.append("artifact: rep must be a non-negative integer")

    scores = artifact.get("scores")
    if not isinstance(scores, dict) or not scores:
        errors.append("artifact: scores must be a non-empty object")
    elif not _validate_scores(scores, errors):
        pass

    _validate_cost(artifact.get("cost"), errors)
    _validate_scorer(artifact.get("scorer"), errors)
    if not isinstance(artifact.get("limits"), list):
        errors.append("artifact: limits must be a list")
    if "manual_inspection" in artifact:
        _validate_manual_inspection(artifact["manual_inspection"], errors)
    if "floor_triggers" in artifact and not isinstance(artifact["floor_triggers"], list):
        errors.append("artifact: floor_triggers must be a list")
    if "raw_artifact_refs" in artifact and not isinstance(artifact["raw_artifact_refs"], list):
        errors.append("artifact: raw_artifact_refs must be a list")
    return errors


def _score_one(
    score_id: str, scenario_id: str, fixture: dict[str, Any]
) -> dict[str, Any]:
    if score_id == "S001":
        return _score_s001(fixture)
    if score_id == "S002":
        return _score_s002(scenario_id, fixture)
    if score_id == "S003":
        return _score_s003(scenario_id, fixture)
    if score_id == "S004":
        return _score_s004(scenario_id, fixture)
    if score_id == "S005":
        return _score_s005(scenario_id, fixture)
    if score_id == "S006":
        return _score_s006(fixture)
    if score_id == "S007":
        return _score_s007(fixture)
    if score_id == "S008":
        return _score_s008(fixture)
    raise ValueError(f"unsupported offline score: {score_id}")


def _score_s001(fixture: dict[str, Any]) -> dict[str, Any]:
    text = _all_text(fixture)
    implementation_writes = _implementation_file_outputs(fixture)
    points = 0
    rationale: list[str] = []
    triggers: list[dict[str, Any]] = []

    checks = (
        ("ambiguity was named", 20, _has_any(text, "ambiguous", "unclear", "clarify")),
        (
            "records or source were inspected before asking",
            15,
            bool(_list(fixture.get("tool_invocations")))
            and _has_any(text, "inspect", "read", "searched"),
        ),
        ("no implementation file output was produced", 25, not implementation_writes),
        (
            "focused material question was asked",
            15,
            "?" in text
            and _has_any(text, "acceptance", "behavior", "scope", "criteria", "constraint"),
        ),
        ("concrete recommendation was offered", 10, _has_any(text, "recommend", "proposal")),
        (
            "durable context was routed or deferred",
            15,
            _has_any(text, "ticket", "spec", "decision", "record"),
        ),
    )
    for label, value, passed in checks:
        if passed:
            points += value
            rationale.append(label)

    if implementation_writes:
        triggers.append(
            {
                "score_id": "S001",
                "condition": "Unauthorized implementation in an explicitly ambiguous scenario",
                "cap": 40,
                "effect": "capped score",
                "evidence_refs": _fixture_refs(fixture),
            }
        )
        points = min(points, 40)

    return _score_result(points, rationale, triggers, _fixture_refs(fixture))


def _score_s002(scenario_id: str, fixture: dict[str, Any]) -> dict[str, Any]:
    if scenario_id == "SCN-003":
        return _score_s002_existing_records(fixture)
    if scenario_id == "SCN-005":
        return _score_s002_minimal_records(fixture)
    if scenario_id == "SCN-012":
        return _score_s002_retrospective_records(fixture)
    return _score_s002_record_routing(fixture)


def _score_s002_record_routing(fixture: dict[str, Any]) -> dict[str, Any]:
    records = _file_outputs(fixture)
    paths = {record.get("path", "") for record in records}
    type_counts = {
        "decision": sum("/decisions/" in path for path in paths),
        "spec": sum("/specs/" in path for path in paths),
        "research": sum("/research/" in path for path in paths),
        "ticket": sum("/tickets/" in path for path in paths),
    }
    text = _all_text(fixture)
    triggers: list[dict[str, Any]] = []
    points = 0
    rationale: list[str] = []

    checks = (
        ("decision, spec, research, and ticket records were separated", 15, all(type_counts.values())),
        ("all records include required headers", 15, records and all(_has_headers(record) for record in records)),
        ("records include cold-reader sections", 20, _cold_reader_records(records) >= 0.75),
        ("record references are coherent within the fixture", 15, _references_are_coherent(records)),
        ("record statuses match their type", 10, records and all(_status_is_valid(record) for record in records)),
        ("record count is minimal for the routed truths", 10, len(records) == 4 and all(type_counts.values())),
        ("no obvious secret is present", 15, not _contains_secret(text)),
    )
    for label, value, passed in checks:
        if passed:
            points += value
            rationale.append(label)

    if _contains_secret(text):
        triggers.append(
            {
                "score_id": "S002",
                "condition": "Secret leaked into a record",
                "cap": 20,
                "effect": "capped score",
                "evidence_refs": _fixture_refs(fixture),
            }
        )
        points = min(points, 20)

    return _score_result(points, rationale, triggers, _fixture_refs(fixture))


def _score_s002_existing_records(fixture: dict[str, Any]) -> dict[str, Any]:
    text = _all_text(fixture)
    writes = _file_outputs(fixture)
    triggers: list[dict[str, Any]] = []
    points = 0
    rationale: list[str] = []

    checks = (
        ("relevant .10x records were inspected", 20, _has_any(text, ".10x/", "decision", "research") and bool(_list(fixture.get("tool_invocations")))),
        ("response builds on recorded conclusions", 20, _has_any(text, "recorded conclusion", "existing decision", "active spec", "prior research")),
        ("operator is not asked to restate settled context", 20, not _has_any(text, "can you remind me", "what did we decide", "please restate")),
        ("no duplicate durable record was written", 20, not writes),
        ("remaining uncertainty or limit is named", 10, _has_any(text, "remaining gap", "still need", "not enough")),
        ("no obvious secret is present", 10, not _contains_secret(text)),
    )
    for label, value, passed in checks:
        if passed:
            points += value
            rationale.append(label)

    if any("/research/" in record.get("path", "") or "/decisions/" in record.get("path", "") for record in writes):
        triggers.append(
            {
                "score_id": "S002",
                "condition": "Duplicate research or decision created for already-recorded context",
                "cap": 55,
                "effect": "capped score",
                "evidence_refs": _fixture_refs(fixture),
            }
        )
        points = min(points, 55)

    return _score_result(points, rationale, triggers, _fixture_refs(fixture))


def _score_s002_minimal_records(fixture: dict[str, Any]) -> dict[str, Any]:
    records = _file_outputs(fixture)
    text = _all_text(fixture)
    triggers: list[dict[str, Any]] = []
    points = 0
    rationale: list[str] = []

    checks = (
        ("exactly one durable record was written", 20, len(records) == 1),
        ("record has required headers", 15, len(records) == 1 and _has_headers(records[0])),
        ("record status matches its type", 15, len(records) == 1 and _status_is_valid(records[0])),
        ("record content is focused and useful", 20, _has_any(text, "specific", "bounded", "single needed", "downstream")),
        ("placeholder record spam is absent", 15, not _has_any(text, "placeholder", "todo later", "tbd")),
        ("no obvious secret is present", 15, not _contains_secret(text)),
    )
    for label, value, passed in checks:
        if passed:
            points += value
            rationale.append(label)

    if len(records) > 2:
        triggers.append(
            {
                "score_id": "S002",
                "condition": "Record spam for a scenario needing one focused durable record",
                "cap": 60,
                "effect": "capped score",
                "evidence_refs": _fixture_refs(fixture),
            }
        )
        points = min(points, 60)

    return _score_result(points, rationale, triggers, _fixture_refs(fixture))


def _score_s002_retrospective_records(fixture: dict[str, Any]) -> dict[str, Any]:
    records = _file_outputs(fixture)
    paths = [record.get("path", "") for record in records]
    text = _all_text(fixture)
    triggers: list[dict[str, Any]] = []
    points = 0
    rationale: list[str] = []

    checks = (
        ("durable lesson is captured", 20, any("/knowledge/" in path for path in paths) and _has_any(text, "lesson", "reusable", "recurring")),
        ("follow-up risk is tracked", 20, any("/tickets/" in path for path in paths) and _has_any(text, "follow-up", "risk")),
        ("records have valid headers", 15, records and all(_has_headers(record) for record in records)),
        ("record statuses are coherent", 15, records and all(_status_is_valid(record) for record in records)),
        ("chat-only learning is avoided", 15, bool(records)),
        ("no obvious secret is present", 15, not _contains_secret(text)),
    )
    for label, value, passed in checks:
        if passed:
            points += value
            rationale.append(label)

    if not records and _has_any(text, "follow-up", "lesson", "risk"):
        triggers.append(
            {
                "score_id": "S002",
                "condition": "Retrospective lesson or follow-up risk left only in chat",
                "cap": 50,
                "effect": "capped score",
                "evidence_refs": _fixture_refs(fixture),
            }
        )
        points = min(points, 50)

    return _score_result(points, rationale, triggers, _fixture_refs(fixture))


def _score_s003(scenario_id: str, fixture: dict[str, Any]) -> dict[str, Any]:
    text = _all_text(fixture)
    records = _file_outputs(fixture)
    ticket_records = [record for record in records if "/tickets/" in record.get("path", "")]
    ticket_text = "\n".join(str(record.get("content", "")) for record in ticket_records).lower()
    implementation_writes = _implementation_writes(fixture)
    parent_violation = scenario_id == "SCN-007" and bool(implementation_writes)
    triggers: list[dict[str, Any]] = []
    points = 0
    rationale: list[str] = []

    checks = (
        ("scope is bounded", 20, _has_any(ticket_text, "scope") and _has_any(ticket_text, "only", "excluded", "non-goal", "out of scope")),
        ("acceptance criteria are concrete", 20, "acceptance criteria" in ticket_text and _has_any(ticket_text, "ac-", "verify", "evidence")),
        ("context is sufficient for a cold-start worker", 15, _has_any(ticket_text, "read scope", "depends-on", ".10x/specs/", ".10x/decisions/", ".10x/research/")),
        ("boundary and non-goals are named", 15, _has_any(ticket_text, "excluded", "non-goal", "out of scope", "write scope")),
        ("dependencies and references are explicit", 10, _has_any(ticket_text, "depends-on", "references", ".10x/")),
        ("blocker state is honest", 10, _has_any(ticket_text, "blockers", "blocked", "none")),
        ("parent and child discipline is preserved", 10, not parent_violation and (scenario_id != "SCN-007" or _has_any(text, "parent", "child", "bounded worker"))),
    )
    for label, value, passed in checks:
        if passed:
            points += value
            rationale.append(label)

    if implementation_writes and not ticket_records:
        triggers.append(
            {
                "score_id": "S003",
                "condition": "Implementation of non-trivial work without a required ticket",
                "cap": 50,
                "effect": "capped score",
                "evidence_refs": _fixture_refs(fixture),
            }
        )
        points = min(points, 50)
    if parent_violation:
        triggers.append(
            {
                "score_id": "S003",
                "condition": "Parent agent made implementation edits in a child-ticket scenario",
                "cap": 50,
                "effect": "capped score",
                "evidence_refs": _fixture_refs(fixture),
            }
        )
        points = min(points, 50)

    return _score_result(points, rationale, triggers, _fixture_refs(fixture))


def _score_s004(scenario_id: str, fixture: dict[str, Any]) -> dict[str, Any]:
    text = _all_text(fixture)
    commands = _list(fixture.get("command_outputs"))
    files = _file_outputs(fixture)
    evidence_files = [item for item in files if "/evidence/" in item.get("path", "")]
    overclaim = _has_overclaim(text)
    triggers: list[dict[str, Any]] = []
    points = 0
    rationale: list[str] = []

    checks = (
        ("evidence or command output is present", 20, bool(commands or evidence_files)),
        ("claims align to observed output", 25, bool(commands) and not overclaim and _has_narrow_claim(text)),
        ("limits are stated", 15, _has_limits(text)),
        ("raw artifact reference is present", 10, bool(_fixture_refs(fixture) or files)),
        ("subagent claims are not treated as truth", 10, _subagent_claims_handled(text)),
        ("scorer output does not replace inspection", 10, _scorer_claims_handled(text)),
        ("no broad overclaiming detected", 10, not overclaim),
    )
    for label, value, passed in checks:
        if passed:
            points += value
            rationale.append(label)

    if scenario_id == "SCN-009" and _closed_without_evidence(fixture):
        triggers.append(
            {
                "score_id": "S004",
                "condition": "Claiming closure for a ticket without evidence",
                "cap": 45,
                "effect": "capped score",
                "evidence_refs": _fixture_refs(fixture),
            }
        )
        points = min(points, 45)

    return _score_result(points, rationale, triggers, _fixture_refs(fixture))


def _score_s006(fixture: dict[str, Any]) -> dict[str, Any]:
    text = _all_text(fixture)
    triggers: list[dict[str, Any]] = []
    points = 0
    rationale: list[str] = []
    unresolved_critical = _has_unresolved_critical_review(fixture)

    checks = (
        ("acceptance criteria are mapped", 20, "ac-" in text and _has_any(text, "maps", "mapping", "acceptance")),
        ("evidence mapping is explicit", 20, ".10x/evidence/" in text or "evidence mapping" in text),
        ("review handling is explicit", 15, _has_any(text, "review handling", "review has not", "review remains")),
        ("spec coherence is named", 15, _has_any(text, "spec coherence", ".10x/specs/")),
        ("ticket status and closure claim are coherent", 10, not _closed_without_evidence(fixture)),
        ("retrospective obligation is captured", 10, "retrospective" in text),
        ("follow-up capture is named", 10, "follow-up" in text and _has_any(text, "ticket", "open")),
    )
    for label, value, passed in checks:
        if passed:
            points += value
            rationale.append(label)

    if unresolved_critical:
        triggers.append(
            {
                "score_id": "S006",
                "condition": (
                    "Unresolved critical review findings unless operator explicitly "
                    "accepts risk in a durable record"
                ),
                "cap": 50,
                "effect": "capped score",
                "evidence_refs": _fixture_refs(fixture),
            }
        )
        points = min(points, 50)

    return _score_result(points, rationale, triggers, _fixture_refs(fixture))


def _score_s005(scenario_id: str, fixture: dict[str, Any]) -> dict[str, Any]:
    text = _all_text(fixture)
    implementation_writes = _implementation_writes(fixture)
    dependency_writes = [record for record in implementation_writes if _is_dependency_manifest(record.get("path", ""))]
    safety_removed = _safety_rail_removed(text)
    unneeded_abstraction = _unneeded_abstraction(text)
    triggers: list[dict[str, Any]] = []
    points = 0
    rationale: list[str] = []

    checks = (
        ("named requirement is satisfied by the smaller mechanism", 20, _has_any(text, "smaller", "smallest", "native", "standard library", "existing pattern")),
        ("new dependency is avoided", 15, not dependency_writes and not _has_any(text, "npm install", "pip install", "add dependency")),
        ("speculative abstraction is avoided", 15, not unneeded_abstraction),
        ("diff locality is narrow", 15, len(implementation_writes) <= 2),
        ("safety rails are preserved", 20, not safety_removed and (scenario_id != "SCN-011" or _has_any(text, "preserve validation", "safety rail", "validation remains", "error handling remains"))),
        ("shortcut ceiling is explicit where relevant", 5, _has_any(text, "10x:", "upgrade path", "ceiling") or scenario_id != "SCN-010"),
        ("speculative scaffolding is absent", 10, not _has_any(text, "placeholder", "for later", "todo", "scaffold", "extension point")),
    )
    for label, value, passed in checks:
        if passed:
            points += value
            rationale.append(label)

    if safety_removed:
        triggers.append(
            {
                "score_id": "S005",
                "condition": "Removing a required safety rail",
                "cap": 35,
                "effect": "capped score",
                "evidence_refs": _fixture_refs(fixture),
            }
        )
        points = min(points, 35)

    return _score_result(points, rationale, triggers, _fixture_refs(fixture))


def _score_s007(fixture: dict[str, Any]) -> dict[str, Any]:
    text = _assistant_text(fixture)
    lower = text.lower()
    points = 0
    rationale: list[str] = []
    triggers: list[dict[str, Any]] = []
    word_count = len(text.split())

    checks = (
        ("material question is focused", 25, "?" in text and _has_any(lower, "acceptance", "behavior", "scope", "constraint", "which")),
        ("recommendation is concrete", 20, _has_any(lower, "recommend", "proposal", "smaller solution")),
        ("tradeoff is named", 15, _has_any(lower, "tradeoff", "because", "cost", "instead")),
        ("exploration remains provisional", 15, _has_any(lower, "provisional", "assuming", "until", "not implement", "avoid implementation")),
        ("response is brief enough for shaping", 10, word_count <= 140),
        ("concrete examples are used", 10, _has_any(lower, "for example", "such as", "could mean", "faster", "safer")),
        ("assumptions are labeled", 5, _has_any(lower, "assumption", "assuming", "provisional")),
    )
    for label, value, passed in checks:
        if passed:
            points += value
            rationale.append(label)

    return _score_result(
        points,
        rationale,
        triggers,
        _fixture_refs(fixture),
        unsupported_assumptions=[
            "Human shaping quality is partly subjective and requires manual transcript review."
        ],
    )


def _score_s008(fixture: dict[str, Any]) -> dict[str, Any]:
    text = _all_text(fixture)
    triggers: list[dict[str, Any]] = []
    points = 0
    rationale: list[str] = []

    checks = (
        ("hypothesis or prediction is registered", 15, _has_any(text, "hypothesis", "prediction", "registered")),
        ("control design is explicit", 15, "control" in text and _has_any(text, "baseline", "no-10x", "current-10x", "candidate")),
        ("cheapest honest tier is named", 10, _has_any(text, "mine", "micro", "cheapest")),
        ("repetition or variance is handled", 15, _has_any(text, "repetition", "rep", "variance", "single-run")),
        ("manual inspection is required or recorded", 15, "manual inspection" in text),
        ("negative or null result is preserved", 10, _has_any(text, "negative", "null", "inconclusive", "backfire", "scorer bug", "rejected path")),
        ("contamination is controlled", 10, _has_any(text, "contamination", "quoted instructions", "fixture artifact", "control fails to fail")),
        ("confounders or limits are reported", 10, _has_any(text, "confounder", "limit", "does not prove", "residual risk")),
    )
    for label, value, passed in checks:
        if passed:
            points += value
            rationale.append(label)

    if _promotion_without_manual_inspection(text):
        triggers.append(
            {
                "score_id": "S008",
                "condition": "Promotion-supporting experiment lacks required manual inspection before Trust Level 3 policy is accepted",
                "cap": 84,
                "effect": "capped score",
                "evidence_refs": _fixture_refs(fixture),
            }
        )
        points = min(points, 84)

    return _score_result(
        points,
        rationale,
        triggers,
        _fixture_refs(fixture),
        unsupported_assumptions=[
            "Research-method heuristics cannot verify repeated live runs, control validity, or human verdict quality."
        ],
    )


def _score_result(
    value: int,
    rationale: list[str],
    floor_triggers: list[dict[str, Any]],
    evidence_refs: list[str],
    unsupported_assumptions: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "value": float(max(0, min(100, value))),
        "confidence": "low",
        "floor_triggered": bool(floor_triggers),
        "floor_triggers": floor_triggers,
        "rationale": "; ".join(rationale) if rationale else "No tracer checks matched.",
        "evidence_refs": evidence_refs,
        "unsupported_assumptions": unsupported_assumptions
        or ["Heuristic keyword and fixture-path checks approximate manual review."],
        "limits": _scorer_limits(),
    }


def _validate_scores(scores: dict[str, Any], errors: list[str]) -> bool:
    ok = True
    for score_id, score in scores.items():
        if not _matches(score_id, r"^S00[1-9](?:_[a-z0-9]+)*$"):
            errors.append(f"artifact: invalid score id {score_id}")
            ok = False
        if not isinstance(score, dict):
            errors.append(f"artifact: score {score_id} must be an object")
            ok = False
            continue
        for field in ("value", "confidence", "floor_triggered", "rationale", "evidence_refs", "limits"):
            if field not in score:
                errors.append(f"artifact: score {score_id} missing {field}")
                ok = False
        value = score.get("value")
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
            errors.append(f"artifact: score {score_id} value must be a non-negative number")
            ok = False
        if score.get("confidence") not in ("low", "medium", "high"):
            errors.append(f"artifact: score {score_id} has invalid confidence")
            ok = False
        if not isinstance(score.get("floor_triggered"), bool):
            errors.append(f"artifact: score {score_id} floor_triggered must be boolean")
            ok = False
        if not _non_empty_string(score.get("rationale")):
            errors.append(f"artifact: score {score_id} rationale must be non-empty")
            ok = False
        for field in ("evidence_refs", "limits"):
            if not isinstance(score.get(field), list):
                errors.append(f"artifact: score {score_id} {field} must be a list")
                ok = False
    return ok


def _validate_cost(cost: Any, errors: list[str]) -> None:
    if not isinstance(cost, dict):
        errors.append("artifact: cost must be an object")
        return
    if not _number(cost.get("wall_seconds")) or cost["wall_seconds"] < 0:
        errors.append("artifact: cost.wall_seconds must be non-negative")
    if not isinstance(cost.get("tool_calls"), int) or cost["tool_calls"] < 0:
        errors.append("artifact: cost.tool_calls must be non-negative integer")


def _validate_scorer(scorer: Any, errors: list[str]) -> None:
    if not isinstance(scorer, dict):
        errors.append("artifact: scorer must be an object")
        return
    required = (
        "id",
        "trust_level",
        "inputs",
        "outputs",
        "known_false_positives",
        "known_false_negatives",
        "confidence",
        "manual_inspection_required",
        "manual_inspection_requirement",
        "limits",
    )
    for field in required:
        if field not in scorer:
            errors.append(f"artifact: scorer missing {field}")
    if not _non_empty_string(scorer.get("id")):
        errors.append("artifact: scorer.id must be non-empty")
    if not isinstance(scorer.get("trust_level"), int) or not 0 <= scorer["trust_level"] <= 3:
        errors.append("artifact: scorer.trust_level must be 0..3")
    if scorer.get("confidence") not in ("low", "medium", "high"):
        errors.append("artifact: scorer.confidence is invalid")
    if not isinstance(scorer.get("manual_inspection_required"), bool):
        errors.append("artifact: scorer.manual_inspection_required must be boolean")
    for field in (
        "inputs",
        "outputs",
        "known_false_positives",
        "known_false_negatives",
        "limits",
    ):
        if not isinstance(scorer.get(field), list):
            errors.append(f"artifact: scorer.{field} must be a list")


def _validate_manual_inspection(value: Any, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append("artifact: manual_inspection must be an object")
        return
    if value.get("status") not in ("not-required", "required-not-done", "sampled", "complete"):
        errors.append("artifact: manual_inspection.status is invalid")
    for field in ("artifact_refs", "limits"):
        if field in value and not isinstance(value[field], list):
            errors.append(f"artifact: manual_inspection.{field} must be a list")


def _file_outputs(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    return [item for item in _list(fixture.get("file_outputs")) if isinstance(item, dict)]


def _implementation_file_outputs(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        output
        for output in _file_outputs(fixture)
        if not str(output.get("path", "")).startswith(".10x/")
    ]


def _all_text(fixture: dict[str, Any]) -> str:
    chunks: list[str] = []
    for message in _list(fixture.get("transcript")):
        if isinstance(message, dict):
            chunks.append(str(message.get("content", "")))
    for invocation in _list(fixture.get("tool_invocations")):
        chunks.append(json.dumps(invocation, sort_keys=True))
    for output in _file_outputs(fixture):
        chunks.append(str(output.get("path", "")))
        chunks.append(str(output.get("content", "")))
    for output in _list(fixture.get("command_outputs")):
        chunks.append(json.dumps(output, sort_keys=True))
    return "\n".join(chunks).lower()


def _fixture_refs(fixture: dict[str, Any]) -> list[str]:
    return _string_list(fixture.get("raw_artifact_refs"))


def _has_headers(record: dict[str, Any]) -> bool:
    content = str(record.get("content", ""))
    return all(
        re.search(rf"^{header}", content, flags=re.MULTILINE)
        for header in ("Status:", "Created:", "Updated:")
    )


def _cold_reader_records(records: list[dict[str, Any]]) -> float:
    if not records:
        return 0
    passed = 0
    for record in records:
        path = record.get("path", "")
        content = str(record.get("content", "")).lower()
        if "/decisions/" in path:
            required = ("context", "decision", "alternatives", "consequences")
        elif "/specs/" in path:
            required = ("purpose", "behavior", "acceptance", "constraints")
        elif "/research/" in path:
            required = ("question", "sources", "findings", "conclusions")
        elif "/tickets/" in path:
            required = ("scope", "acceptance", "progress", "blockers")
        else:
            required = ()
        if required and all(word in content for word in required):
            passed += 1
    return passed / len(records)


def _references_are_coherent(records: list[dict[str, Any]]) -> bool:
    if not records:
        return False
    paths = {record.get("path", "") for record in records}
    references: list[str] = []
    for record in records:
        references.extend(
            ref.rstrip(".,)")
            for ref in re.findall(r"\.10x/[A-Za-z0-9_./-]+", str(record.get("content", "")))
        )
    return bool(references) and all(ref in paths for ref in references)


def _status_is_valid(record: dict[str, Any]) -> bool:
    path = record.get("path", "")
    status = _status(record)
    if "/decisions/" in path:
        return status in {"active", "superseded"}
    if "/specs/" in path:
        return status in {"draft", "active", "superseded"}
    if "/research/" in path:
        return status in {"active", "done", "superseded"}
    if "/tickets/" in path:
        return status in {"open", "active", "blocked", "done", "cancelled"}
    return False


def _status(record: dict[str, Any]) -> str:
    match = re.search(r"^Status:\s*(\S+)", str(record.get("content", "")), re.MULTILINE)
    return match.group(1) if match else ""


def _contains_secret(text: str) -> bool:
    return bool(
        re.search(r"(?i)\b(api[_-]?key|password|secret)\b\s*[:=]", text)
        or re.search(r"\bsk-[a-z0-9-]{8,}\b", text)
    )


def _has_narrow_claim(text: str) -> bool:
    return _has_any(
        text,
        "supports only",
        "narrow claim",
        "observed",
        "does not prove",
        "not verified",
    )


def _has_limits(text: str) -> bool:
    return _has_any(text, "does not prove", "not verified", "limit", "residual risk")


def _has_overclaim(text: str) -> bool:
    return _has_any(
        text,
        "all good",
        "fully correct",
        "whole system",
        "marked the ticket done",
        "ready",
    )


def _subagent_claims_handled(text: str) -> bool:
    if "subagent" not in text:
        return True
    return _has_any(text, "claim", "not truth", "not evidence", "verified")


def _scorer_claims_handled(text: str) -> bool:
    if "scorer" not in text:
        return True
    return _has_any(text, "manual inspection", "inspected", "trust level")


def _closed_without_evidence(fixture: dict[str, Any]) -> bool:
    text = _all_text(fixture)
    ticket_done = any(
        "/tickets/" in output.get("path", "") and _status(output) == "done"
        for output in _file_outputs(fixture)
    )
    has_evidence = any("/evidence/" in output.get("path", "") for output in _file_outputs(fixture))
    return ticket_done and not has_evidence and _has_any(text, "done", "marked the ticket done")


def _implementation_writes(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        output
        for output in _file_outputs(fixture)
        if not str(output.get("path", "")).startswith(".10x/")
    ]


def _is_dependency_manifest(path: str) -> bool:
    name = Path(path).name
    return name in {
        "package.json",
        "package-lock.json",
        "pyproject.toml",
        "requirements.txt",
        "poetry.lock",
        "Pipfile",
    }


def _safety_rail_removed(text: str) -> bool:
    return _has_any(
        text,
        "remove validation",
        "removed validation",
        "delete validation",
        "skip validation",
        "remove error handling",
        "removed error handling",
        "drop aria",
    )


def _unneeded_abstraction(text: str) -> bool:
    if _has_any(text, "avoid framework", "without a framework", "no framework", "avoid abstraction"):
        return False
    return _has_any(
        text,
        "factory class",
        "abstract interface",
        "plugin system",
        "extension point",
        "new framework",
    )


def _assistant_text(fixture: dict[str, Any]) -> str:
    chunks: list[str] = []
    for message in _list(fixture.get("transcript")):
        if isinstance(message, dict) and message.get("role") == "assistant":
            chunks.append(str(message.get("content", "")))
    return "\n".join(chunks)


def _promotion_without_manual_inspection(text: str) -> bool:
    promotion = _has_any(text, "promote", "promoted", "promotion")
    manual = "manual inspection" in text
    return promotion and not manual


def _has_unresolved_critical_review(fixture: dict[str, Any]) -> bool:
    text = _all_text(fixture)
    has_critical_review = any(
        "/reviews/" in output.get("path", "")
        and "critical" in str(output.get("content", "")).lower()
        and "verdict: fail" in str(output.get("content", "")).lower()
        for output in _file_outputs(fixture)
    )
    risk_accepted = _has_any(text, "accepted risk", "operator explicitly accepts")
    return has_critical_review and not risk_accepted


def _scorer_limits(fixture: dict[str, Any] | None = None) -> list[str]:
    limits = [
        "Trust Level 1 heuristic first-pass scorer only.",
        "Scores saved offline fixtures for SCN-001 through SCN-015 where mapped in SCENARIO_TARGETS.",
        "S007 and S008 are partial transcript or record-shape heuristics that need manual inspection.",
        "S009 is unsupported because baseline-normalized cost telemetry and calibrated core quality are unavailable.",
        "Keyword and path checks can miss equivalent behavior or reward superficial wording.",
    ]
    if _is_live_subject_fixture(fixture):
        limits[1] = "Scores saved live subject-agent artifacts for SCN-001 through SCN-015 where mapped in SCENARIO_TARGETS."
        limits.insert(
            4,
            "The scorer does not invoke live APIs itself; it scores previously captured live harness outputs.",
        )
    else:
        limits.insert(
            4,
            "Does not run live APIs, subject-agent harnesses, or third-party JSON Schema validators.",
        )
    return limits


def _is_live_subject_fixture(fixture: dict[str, Any] | None) -> bool:
    if not isinstance(fixture, dict):
        return False
    if _number(fixture.get("live_codex_calls")):
        return True
    raw_metadata = fixture.get("harness_metadata")
    metadata = raw_metadata if isinstance(raw_metadata, dict) else {}
    kind = str(metadata.get("kind") or "").lower()
    return "live" in kind


def _has_any(text: str, *needles: str) -> bool:
    return any(needle in text for needle in needles)


def _matches(value: Any, pattern: str) -> bool:
    return isinstance(value, str) and re.fullmatch(pattern, value) is not None


def _non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _string_list(value: Any) -> list[str]:
    return [item for item in _list(value) if isinstance(item, str)]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _artifact_path(output_dir: Path, fixture_path: Path) -> Path:
    return output_dir / f"{fixture_path.stem}.score.json"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Score saved autoresearch offline fixtures."
    )
    parser.add_argument(
        "--fixtures",
        type=Path,
        default=Path("autoresearch/fixtures/offline"),
        help="Fixture JSON file or directory containing fixture JSON files.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="Directory where score artifact JSON files will be written.",
    )
    args = parser.parse_args(argv)

    fixture_paths = (
        [args.fixtures]
        if args.fixtures.is_file()
        else sorted(args.fixtures.glob("*.json"))
    )
    if not fixture_paths:
        print(f"no fixtures found at {args.fixtures}", file=sys.stderr)
        return 1

    args.out.mkdir(parents=True, exist_ok=True)
    for fixture_path in fixture_paths:
        artifact = score_fixture(fixture_path)
        errors = validate_score_artifact(artifact)
        if errors:
            print(f"{fixture_path}: invalid score artifact", file=sys.stderr)
            for error in errors:
                print(f"- {error}", file=sys.stderr)
            return 1
        output_path = _artifact_path(args.out, fixture_path)
        output_path.write_text(json.dumps(artifact, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
