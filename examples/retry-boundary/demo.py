"""Synthetic retry-boundary example; no network, real bookings, or private runtime.

Run with Python 3.10+ and its standard library: python3 -I -B demo.py
SQLite is both the local fake service and its evidence store. This is NOT an
exactly-once guarantee for a remote provider, production code, or a customer test.
"""
from __future__ import annotations

import json
import sqlite3
import tempfile
from dataclasses import dataclass, replace
from pathlib import Path


@dataclass(frozen=True)
class Booking:
    recipient: str
    slot: str

    def payload(self) -> str:
        return json.dumps({"recipient": self.recipient, "slot": self.slot}, sort_keys=True)


@dataclass(frozen=True)
class Approval:
    # Fixture input, not a signed authorization or real identity system.
    approved_payload: str
    expires_at: int
    revoked: bool = False

    def permits(self, booking: Booking, now: int) -> bool:
        return not self.revoked and now < self.expires_at and booking.payload() == self.approved_payload


class KeyConflict(ValueError):
    pass


class FakeBookingService:
    def __init__(self, path: Path, deduplicate: bool):
        self.path = path
        self.deduplicate = deduplicate
        self.calls = 0
        self.db = sqlite3.connect(str(path))
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY, request_key TEXT NOT NULL, payload TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS receipts (
                request_key TEXT PRIMARY KEY, payload TEXT NOT NULL, booking_id INTEGER NOT NULL);
        """)

    def book(self, request_key: str, booking: Booking, lose_ack: bool = False) -> str:
        self.calls += 1
        payload = booking.payload()
        with self.db:
            # Explicit transaction: the fixture's effect and receipt share one DB.
            self.db.execute("BEGIN IMMEDIATE")
            row = self.db.execute(
                "SELECT payload, booking_id FROM receipts WHERE request_key = ?", (request_key,)
            ).fetchone() if self.deduplicate else None
            if row is not None:
                if row[0] != payload:
                    raise KeyConflict("same key, different payload")
                acknowledgement = "EXISTING_BOOKING_CONFIRMED"
            else:
                cursor = self.db.execute(
                    "INSERT INTO bookings(request_key, payload) VALUES (?, ?)", (request_key, payload)
                )
                if self.deduplicate:
                    self.db.execute("INSERT INTO receipts VALUES (?, ?, ?)",
                                    (request_key, payload, cursor.lastrowid))
                acknowledgement = "NEW_BOOKING_CONFIRMED"
        # Fault injection occurs AFTER commit. The caller cannot infer the outcome.
        if lose_ack:
            raise TimeoutError("simulated lost acknowledgement after commit")
        return acknowledgement

    def observed_effects(self) -> int:
        # Harness observation from a separate connection, not the client's status.
        other = sqlite3.connect(str(self.path))
        try:
            return other.execute("SELECT COUNT(*) FROM bookings").fetchone()[0]
        finally:
            other.close()

    def close(self) -> None:
        self.db.close()


def attempt(service: FakeBookingService, key: str, booking: Booking,
            approval: Approval, now: int = 10, lose_ack: bool = False) -> str:
    if not approval.permits(booking, now):
        return "APPROVAL_DENIED"
    try:
        return service.book(key, booking, lose_ack)
    except TimeoutError:
        return "OUTCOME_UNKNOWN"
    except KeyConflict:
        return "IDEMPOTENCY_KEY_CONFLICT"
    # There is intentionally no automatic retry or conversion of unknown to success.


def run_demo() -> dict:
    booking = Booking("synthetic-recipient", "synthetic-slot")
    approval = Approval(booking.payload(), expires_at=20)
    rows = []
    with tempfile.TemporaryDirectory(prefix="okira22-public-demo-") as temp:
        for name in ("normal", "unsafe_retry", "guarded_retry", "unknown_without_retry",
                     "changed_payload", "expired_approval", "revoked_approval",
                     "key_payload_conflict", "database_reopen"):
            path = Path(temp) / (name + ".sqlite")
            service = FakeBookingService(path, deduplicate=name != "unsafe_retry")
            try:
                states = []
                effects_after_first = None
                if name in ("unsafe_retry", "guarded_retry", "database_reopen"):
                    states.append(attempt(service, "operation-1", booking, approval, lose_ack=True))
                    effects_after_first = service.observed_effects()
                    first_calls = service.calls
                    if name == "database_reopen":
                        service.close()
                        service = FakeBookingService(path, deduplicate=True)
                    states.append(attempt(service, "operation-1", booking, approval))
                    calls = first_calls + service.calls if name == "database_reopen" else service.calls
                elif name == "key_payload_conflict":
                    states.append(attempt(service, "operation-1", booking, approval))
                    changed = replace(booking, slot="other-synthetic-slot")
                    # A new fixture approval is not permission to reuse a key for new data.
                    states.append(attempt(service, "operation-1", changed,
                                          Approval(changed.payload(), expires_at=20)))
                    calls = service.calls
                else:
                    payload = replace(booking, recipient="other-synthetic-recipient") if name == "changed_payload" else booking
                    permission = replace(approval, revoked=True) if name == "revoked_approval" else approval
                    now = 20 if name == "expired_approval" else 10
                    states.append(attempt(service, "operation-1", payload, permission,
                                          now, lose_ack=name == "unknown_without_retry"))
                    calls = service.calls
                effects = service.observed_effects()
                rows.append({"case": name, "client_states": states,
                             "service_calls": calls, "observed_booking_rows": effects,
                             "effects_after_first_attempt": effects_after_first,
                             "workflow_result": "FAIL_DUPLICATE_EFFECT" if effects > 1
                             else "OUTCOME_UNKNOWN" if states[-1] == "OUTCOME_UNKNOWN"
                             else "DENIED_BEFORE_SERVICE" if states[-1] == "APPROVAL_DENIED" and calls == 0
                             else "CONFLICT_REJECTED" if states[-1] == "IDEMPOTENCY_KEY_CONFLICT" else "EXPECTED_BEHAVIOR"})
            finally:
                service.close()
    return {"example": "Okira22 public retry-boundary demonstration", "synthetic_only": True,
            "network_requests": 0, "customer_system_tested": False,
            "process_restart_tested": False, "database_reopen_tested": True,
            "cases": rows,
            "limits": ["Local fake service and receipt use one SQLite transaction.",
                       "No remote API, crash/power-loss, concurrency or load testing.",
                       "Approval is fixture data, not cryptographic authentication.",
                       "No guarantee of exactly-once external effects."]}


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 1:
        raise SystemExit("No arguments: this example accepts only built-in synthetic fixtures.")
    print(json.dumps(run_demo(), indent=2))
