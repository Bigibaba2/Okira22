# Retry boundary: a small, reproducible pilot example

**Question:** a booking is committed, its acknowledgement is lost, and the caller tries again. Does the workflow create a duplicate or reconcile the original action?

**What this is:** a newly written public teaching example for the Okira22 Runtime Reliability Pilot. The code actually runs a local fake booking service and reads its SQLite records from a separate connection. All identities, slots, approvals and effects are synthetic. It does not import the private runtime, contact a website, send a message or create a real booking.

## Reproduce

Use a reviewed local checkout, Python 3.10+ with the standard-library `sqlite3` module, and run from the repository root:

```bash
python3 -I -B examples/retry-boundary/test_demo.py
python3 -I -B examples/retry-boundary/demo.py
```

There are no packages to install, credentials to configure or elevated permissions to grant. Each run creates only disposable SQLite files in a new temporary directory and removes them when the run completes. The demonstration takes no target, path or account arguments.

The checked execution used **Python 3.13.5 / SQLite 3.46.1 / Linux x86_64**, on **2026-10-05**, in the isolated conversation execution container. Other Python/OS combinations have not been tested here. See [raw test output](test-results.txt) and [recorded JSON](results.json). Timing in the test log is not a benchmark.

## Observed results

| Synthetic scenario | Service calls | Booking rows | Observed outcome |
| --- | ---: | ---: | --- |
| Ordinary acknowledged request | 1 | 1 | A new booking is confirmed |
| Deliberately unsafe retry after lost acknowledgement | 2 | **2** | **FAIL: duplicate effect reproduced** |
| Same retry with key/payload receipt and atomic local deduplication | 2 | **1** | Existing booking confirmed, no second local effect |
| Lost acknowledgement, no retry | 1 | 1 | Caller correctly retains **OUTCOME_UNKNOWN** |
| Payload changed after fixture approval | 0 | 0 | Denied before the service is called |
| Approval expires at the test boundary | 0 | 0 | Denied before the service is called |
| Approval revoked before the attempt | 0 | 0 | Denied before the service is called |
| Same key, different payload, new fixture approval | 2 | 1 | Conflicting key reuse rejected |
| Close/reopen database, then retry original operation | 2 | 1 | Stored receipt reused; no duplicate local effect |

**12 assertion tests passed.** Passing tests include asserting that the deliberately unsafe variant fails its workflow goal. That does not turn a duplicate booking into a PASS. Nine scenarios and 12 assertions are not 21 tests, and repeated runs are not additional unique cases.

The fault is injected **after** the first SQLite transaction commits. The effect therefore remains visible to the harness while the caller sees a timeout. The harness's separate connection is evidence inside our own fixture—not an independent third-party audit. The client does not claim success merely because the harness can see a row.

## What the comparison supports

Within this one-transaction local fake service, a stable operation key bound to the payload allows the second attempt to recover the existing result. Expired, revoked or changed fixture approvals prevent a service call. Without a usable acknowledgement, the caller preserves uncertainty instead of guessing success or failure.

The example does **not** prove exactly-once behavior across external services. A real provider may have different key retention, payload checks, reconciliation, side effects and failure boundaries. A local record written separately from a remote action is not an atomic transaction with that action. Those are questions to test in an agreed pilot, not assumptions supplied by this demo.

## Not tested / not implemented

No real identity or signed approval system, network timeout, process crash, power loss, concurrent workers, load, external provider, retention expiry, production deployment or confidential customer data was tested. The connection-reopen case is **not** a process-restart test. There is no automatic retry engine. This example is educational code, not a drop-in production control or a resume of autonomous hunting.

A test runs all scenarios with Python socket creation, connection and DNS-resolution entry points patched to raise; the source itself uses no network client. This is not a general operating-system sandbox proof.

## Source fingerprint for the recorded result

- `demo.py` SHA-256: `69fbb15832751b7e83369225a34e226a2f27c39a7eacc5f154c645faa44527a6`
- `test_demo.py` SHA-256: `d00cd784b7b4ad4856cd5946d93fccf217b59758b122eec378d46e4ab1cd4f08`

These public digests identify checked bytes; they are not a signature or source-authentication claim. Review the source and reproduce the result yourself. The two input source files, recorded JSON, raw test log and this explanation are deliberately public; no private project or client material was exported.

## Apply this approach to your workflow

The [$222 pilot](../../docs/PILOT.md) maps **one agreed workflow**, selects its meaningful failure cases, and produces reproducible checks, evidence and prioritized recommendations. We first confirm a suitable staging or synthetic reproduction. Results and payment terms are agreed in the written scope; no customer defect or delivery feasibility is presumed by this example.

[Evidence and reporting approach](../../docs/TRUST_AND_EVIDENCE.md) · [Project overview](../../README.md)
