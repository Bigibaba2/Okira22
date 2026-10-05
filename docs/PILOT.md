# Okira22 Runtime Reliability Pilot

**One workflow. Reproducible checks. Clear evidence.**

| Item | Proposed engagement |
| --- | --- |
| Price | $222 USD fixed |
| Scope | One explicitly agreed AI-agent or automation workflow |
| Delivery | 2–3 business days after written scope and required inputs/access are agreed |
| Environment | Client-approved staging, synthetic fixtures, or an agreed local reproduction |
| Delivery owner | Armin Ahoei, founder of Okira22 |

The pilot is a human-led engineering review supported by tooling. It does not require a claim that the complete Okira22 runtime is production-ready.

## Before work begins

We identify the action, its intended authority, expected effects and observable result. We then confirm that a representative reproduction and the necessary evidence are available within the pilot's scope. If they are not, we adjust the scope before accepting the work rather than promise an unsupported delivery date.

The written scope records the selected cases, access and data-handling permissions, acceptance criteria, delivery date and payment terms. One path means one path—not a review of every integration in a product.

## Example checks

Select the checks relevant to the actual workflow. These are examples, not claims that any customer's system has these faults:

- An approval expires or is withdrawn before the action starts.
- The recipient, payload or amount changes after approval.
- A duplicate event or retry could trigger a repeated effect.
- A request times out and the external outcome is uncertain.
- A workflow reports success without enough supporting execution evidence.

Negative tests run only inside the agreed environment. No real payments, customer messages, production mutations or new third-party targets are authorized by the proposal alone.

## Deliverables

**Boundary map:** a compact description of the action, approval, identities, state transitions and systems involved.

**Reproducible checks:** the agreed test cases, setup assumptions, sanitized fixtures or scripts where sharing is permitted, and instructions for running them again.

**Evidence report:** PASS, FAIL, INCONCLUSIVE or NOT TESTED for each case, with expected behavior, actual observation, evidence references and limitations. A successful API response alone is not treated as proof of the intended business outcome.

**Prioritized recommendations:** practical fixes or additional checks, clearly separated from changes already implemented. Production remediation is not included by default.

## What we need from you

Start with a brief workflow description and the action that matters most. After agreeing confidentiality and handling requirements, we may request a minimal sanitized example, a staging reproduction or permission to inspect the relevant code. Do not send raw credentials or customer records in an introductory email.

For healthcare workflows, the initial scope excludes patient information. For financial actions, use synthetic or sandbox transactions. Any broader access requires a separate explicit agreement.

## Acceptance and limitations

Delivery means the agreed artifacts and documented outcomes are provided—not that every case passes. Missing observability is reported as a limitation, not disguised as a successful verification. An inconclusive result includes the specific evidence or reproduction needed next.

This is not a whole-system audit, compliance assessment, certification, guarantee of no defects, or promise of a vulnerability finding. Additional workflows, extensive integration work, deployment, production fixes and ongoing monitoring are outside the fixed pilot scope unless separately agreed.

**Next step:** send a short description of one workflow to [outreach@bigiraden.com](mailto:outreach@bigiraden.com). The response will be a proposed scope, not an automatic start of testing.

[Back to the project](../README.md) · [Evidence approach](TRUST_AND_EVIDENCE.md)
