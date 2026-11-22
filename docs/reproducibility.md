# Reproducibility package (MT7, Subtask 7.3)

**Status:** 2026-11-21. This describes how to verify every frozen artifact and
every erratum, and what cannot be reproduced. "Reproduced" below always means
**internal recomputation by the project**, not third-party validation.

## 0. Archived release binding

The fixed MT7 synthesis snapshot is bound to the following public identifiers:

| Field | Value |
|---|---|
| Repository commit | `66feb06de421d43d928a6ed17ee63ba573778191` |
| GitHub release | [`v1.0.0-mt7-synthesis`](https://github.com/Raina-ya/sense-correct-abstain/releases/tag/v1.0.0-mt7-synthesis) |
| Zenodo version DOI | [`10.5281/zenodo.24443391`](https://doi.org/10.5281/zenodo.24443391) |
| Zenodo concept DOI | [`10.5281/zenodo.24443390`](https://doi.org/10.5281/zenodo.24443390) |
| Archive filename | `sense-correct-abstain-v1.0.0-mt7-synthesis-66feb06.zip` |
| Archive SHA-256 | `8038aad3ede75a37b5ffd7b20bfcba26258c0c42b88a631923d03b040e1ee1b6` |

The version DOI and archive hash identify the immutable public snapshot. Later
repository commits may improve discovery or documentation, but they do not
alter that archived version. Scientific claims remain governed by the frozen
records and append-only errata inside the snapshot.

## 1. Environment record of the frozen artifacts

| Artifact | Producer | Python | Platform | NumPy | Other packages |
|---|---|---|---|---|---|
| Gate 1A/1B (`results/gate1a/`, `results/gate1b/`) | `tools/run_gate1a.py`, `tools/run_gate1b.py` | **unknown** | **unknown** | not used (standard library only) | none |
| Gate 2 (`results/dev/`) | `tools/run_gate2.py` | **unknown** | **unknown** | **2.3.5** (recorded in the artifact) | none |
| Gates 3/4 (`results/gate34/`) | `tools/run_gate34.py` | **unknown** | **unknown** | **2.3.5** (recorded in the artifact) | none |

`requirements.txt` pins `numpy==2.3.5` to match the recorded version. Its
`pytest>=8` line is for running the tests and did not produce any artifact.
The Python version and platform of the original runs were never recorded and
are not guessed here.

## 2. Verification commands

```bash
pip install -r requirements.txt
python -m pytest -q tests                      # unit tests, including the errata and lock-template tests
python -m unittest discover -s tests           # same tests without pytest (standard library only)
python tools/check_errata_artifacts.py         # errata manifests v1-v6, plus every frozen lock/artifact check
python tools/check_rc_semantics.py             # 64 label-angle RC equivalence cases
python tools/check_pamp_semantics.py           # 729 P-amp circuit cases vs the phase model
python tools/check_library.py                  # literature library structure
python tools/check_archive_manifest.py         # public archive metadata and cross-document consistency
python tools/audit_gate34_estimand.py          # reproduces the frozen Gate 3 numbers, then the corrected estimand
python tools/audit_reproducibility.py 50       # sampled recomputation of Gate 2 and Gate 3/4 units (about 1 minute)
python tools/audit_reproducibility.py 1        # full recomputation (several minutes)
```

The frozen runners refuse to rerun: their outputs exist, and they require
`HEAD` to equal their lock commit. They are not meant to be re-executed. The
recomputation tool calls their per-unit functions without writing anything.

The fast, read-only subset of these commands (unit tests, errata and frozen
lock/artifact checks, archive manifest, RC and P-amp semantics, library) also
runs on every push via `.github/workflows/checks.yml`. Those runs are internal
recomputation on GitHub-hosted runners, not third-party validation; the audit
and recomputation tools are not run in CI.

## 3. Hash manifests

| Manifest | Covers | Checker |
|---|---|---|
| `docs/freeze/gate1_design_lock_manifest.sha256` | M3 design (documents only) | `tools/check_gate1_lock.py` |
| `results/gate1_artifact_manifest.sha256` | Gate 1 code, results, reports | `tools/check_gate1_artifacts.py` |
| `docs/freeze/gate2_dev_design_manifest.sha256`, `results/gate2_artifact_manifest.sha256` | Gate 2 | `check_gate2_lock.py`, `check_gate2_artifacts.py` |
| `docs/freeze/gate3_gate4_design_manifest.sha256`, `results/gate34_artifact_manifest.sha256` | Gates 3/4 | `check_gate34_lock.py`, `check_gate34_artifacts.py` |
| `results/errata/errata_manifest.sha256` (v1), `results/errata/errata_manifest_v2.sha256` | v1: errata E001–E005 and their tools, outputs, and `requirements.txt` (`project_status.md` is checked against commit `9201ba9`). v2: E006, its tools and outputs, and the lock-template policy. MT7 drafts are deliberately not hashed. | `tools/check_errata_artifacts.py` |

All hashes are SHA-256 after CRLF-to-LF canonicalization.

## 4. What reproduces and what does not

| Property | Result | Source |
|---|---|---|
| Frozen Gate 3 `Delta_V` and lower bound from stored per-unit fields | exact | `tools/audit_gate34_estimand.py` |
| Gate 2 and Gate 3/4 verdict-level fields under full recomputation (Linux, Python 3.13.18, NumPy 2.3.5) | identical | `results/errata/reproducibility_full.json` |
| Same, sampled (Linux, Python 3.10.12, NumPy 2.2.6) | identical | E005 §4 |
| Stored per-unit floats across platforms | **not** bit-identical: 416 of 6600 (Gate 2) and 31 of 5940 (Gate 3/4) units differ | E005 §4 |
| Code precedence over results (code existing before each run) | **cannot be shown**: code was outside every lock | E005 §1 |
| Hardware behavior | not studied | — |

**Cause of the float differences:** last-bit platform differences in computed
probabilities change an occasional multinomial count. Future locks must
round probabilities before sampling or record the platform
(`docs/protocols/lock_template_v2.md`).

## 5. Future locked work

Use `docs/protocols/lock_template_v2.md` and `tools/check_protocol_lock.py`.
A v2 lock hashes the runner, every imported module, the tests, the
environment, the seeds, and the command, and it refuses an "unknown"
environment.
