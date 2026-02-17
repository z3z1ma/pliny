from __future__ import annotations

import unittest
from dataclasses import dataclass
from typing import Any, cast

from agent_loom.ticket.errors import TicketArgError, TicketNotFoundError
from agent_loom.ticket.store import TicketStore
from agent_loom.ticket.update_workflow import _validate_parent_chain


@dataclass
class _FakeTicket:
    fm: dict[str, Any]


class _FakeStore:
    def __init__(self, parents: dict[str, str]) -> None:
        self._parents = dict(parents)

    def load_ticket_by_id(self, ticket_id: str) -> _FakeTicket:
        if ticket_id not in self._parents:
            raise TicketNotFoundError(code="NOT_FOUND", error=f"missing: {ticket_id}")
        return _FakeTicket(fm={"parent": self._parents[ticket_id]})


class TestValidateParentChain(unittest.TestCase):
    def test_rejects_existing_parent_cycle_in_chain(self) -> None:
        store = _FakeStore(
            {
                "al-2": "al-3",
                "al-3": "al-2",
            }
        )
        with self.assertRaises(TicketArgError) as ctx:
            _validate_parent_chain(
                cast(TicketStore, store), ticket_id="al-1", parent_id="al-2"
            )
        self.assertIn("cycle", str(ctx.exception).lower())
        self.assertEqual(ctx.exception.code, "ARG")

    def test_rejects_missing_ticket_in_chain(self) -> None:
        store = _FakeStore({"al-2": "al-missing"})
        with self.assertRaises(TicketArgError) as ctx:
            _validate_parent_chain(
                cast(TicketStore, store), ticket_id="al-1", parent_id="al-2"
            )
        self.assertIn("missing ticket", str(ctx.exception).lower())
        self.assertEqual(ctx.exception.code, "ARG")


if __name__ == "__main__":
    unittest.main()
