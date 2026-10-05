# Historical controlled-launch release

**Status as of 2026-10-05: legacy reference; not the current pilot onboarding path.**

The March 2026 controlled-launch package and installer belong to an earlier distribution
experiment. The current offer is the [Runtime Reliability Pilot](PILOT.md): one agreed
workflow reviewed by the founder with client-approved staging or synthetic inputs.
Customers do not need to install the old package to discuss or begin that pilot.

## What was retired

The root `install.sh` now prints a retirement notice and exits with status 1. It does not
download a package, request elevated privileges, invoke a package manager or modify a
system. This intentionally changes the behavior of the mutable `main/install.sh` URL;
existing automation that used it will stop rather than install an older package.

The original installer bytes are preserved as
[`archive/controlled-launch/install.sh.txt`](../archive/controlled-launch/install.sh.txt)
for historical inspection, not execution. Its original Git blob is
`4b16eee0f154cd20a30c9e77f0c04a3696ff238f`, also available in commit
`4d9a5025eccfb1f9a49b75a74b513fd7ec95adf5`.

## Historical release inventory

| Item | Observed value |
| --- | --- |
| Tag | `v1.0.0-controlled-launch` |
| Release title at review | `Okira22 — Controlled Launch` |
| Published | 2026-03-27 |
| Release classification | Prerelease |
| Asset | `okira22_1.0.1-10_all.deb` |
| Asset size reported by GitHub | 48,180 bytes |
| Asset SHA-256 reported by GitHub | `1b29e28ea07f8037bf67ce61150ece7213821bb0c333881afebccc4f4af38b96` |

These values were read from GitHub release metadata. The binary was not downloaded,
executed or independently validated in this review. The listed digest is inventory
information, not proof that a client verified a download.

The existing release page, tag, assets and older Git commits are retained unchanged.
This file is a retirement notice in the current repository, **not deletion, unpublishing
or modification of that release**. Historical scripts fetched through old commit/tag URLs
retain their old behavior. Existing installations are not changed or uninstalled.

## Why separate it from the pilot?

The historical script required root, downloaded a package to a predictable temporary
path, followed redirects and invoked `apt update` and `apt install`. It checked that the
download was nonempty but did not compare it with a pinned digest before installation.
Those are source observations, not a finding that the package is malicious or that any
installed system was compromised.

Package suitability for a particular system has not been revalidated here. The pilot is
a scoped engineering service, not a self-service deployment of this historical runtime.

## Returning to distribution later

Review package provenance, integrity verification, installation side effects, supported
environments and rollback behavior before publishing a newly supported installation
path. Do not silently reactivate the archived installer or imply that the pilot's
documentation certifies the old release.

[Current pilot](PILOT.md) · [Project overview](../README.md)
