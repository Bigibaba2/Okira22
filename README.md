# Okira22

**Trust through evidence.**

Okira22 is a founder-led project focused on the reliability and security boundaries of AI agents and automation: what an action was allowed to do, what actually happened, and what the evidence can establish.

## A focused service, not a promise of autonomous security

The current offer is a **Runtime Reliability Pilot: $222 USD fixed for one agreed workflow**.

Working with your staging environment or synthetic fixtures, Armin Ahoei reviews one consequential action path and tests the failure cases agreed in advance. Examples include expired approval, a changed payload, duplicate delivery, a timeout after an action, or a success message that cannot be reconciled with execution evidence.

You receive a boundary map, reproducible tests, a concise evidence report, and prioritized fix recommendations. The proposed delivery window is **2–3 business days after written scope and the required inputs/access are agreed**. Feasibility is checked before accepting the engagement.

**Start with one workflow. No production access or sensitive customer data is required for the initial scoping discussion.**

[Read the pilot scope](docs/PILOT.md) · [See our evidence approach and report example](docs/TRUST_AND_EVIDENCE.md)

## Run a small public example

What happens when a booking is committed but the acknowledgement is lost? Our [retry-boundary example](examples/retry-boundary/README.md) includes source, reproduction commands and recorded synthetic results. The deliberately unsafe retry produces two local booking rows; the guarded variant preserves one. Unknown outcomes remain unknown until evidence is available.

The example has **12 passing assertion tests across nine synthetic scenarios**, executed locally—not a GitHub CI result, customer audit or production benchmark. No credentials, network connection or installer are needed. The private runtime is not included.

## Project status

| Area | What this repository represents |
| --- | --- |
| Paid pilot | A limited, founder-led, human-reviewed service; scope is agreed before work |
| Runtime and research tooling | Development work, not a claim of general production readiness |
| Autonomous bug-bounty hunting | Not offered as a production-ready capability |
| User interface | Under development; not a prerequisite for the pilot |
| Public repository | Project overview and service documentation, not the complete private runtime |

An internal test result is not a customer audit. A simulated example is not a production finding. We distinguish observed results from assumptions and explicitly record anything not tested.

## What we do not promise

A pilot is not a security certification, a full application penetration test, a guarantee of finding vulnerabilities, a guaranteed bounty, or continuous monitoring. Remediation, production changes and additional workflows require a separate agreement.

## Historical installer

The earlier controlled-launch installer is **retired from the current onboarding path**. The root `install.sh` now prints a notice and exits without downloading or installing anything. The original script is preserved as archival text; historical release assets and existing installations are unchanged. See the [legacy release inventory and limitations](docs/LEGACY_RELEASES.md).

**No installer is needed for the $222 pilot. Start with an agreed workflow and scope.**

## Contact

**Armin Ahoei — Founder, Okira22**

Website: [bigiraden.com](https://bigiraden.com)  
Pilot enquiries: [outreach@bigiraden.com](mailto:outreach@bigiraden.com)

For an initial enquiry, describe one workflow, its approval boundary and the failure you most want to understand. Do not send passwords, API tokens, session cookies, medical information or private customer records.

For security concerns about this repository, see [SECURITY.md](SECURITY.md).
