"""Check the public archive manifest and its repository references."""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "archive" / "manifest.json"
SHA256 = re.compile(r"[0-9a-f]{64}")
COMMIT = re.compile(r"[0-9a-f]{40}")


def main() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    required = {
        "schema", "version", "repository_commit", "github_release",
        "zenodo_record", "version_doi", "concept_doi", "archive",
    }
    if set(data) != required:
        raise SystemExit("archive manifest fields do not match schema v1")
    if data["schema"] != "sense-correct-abstain/archive-manifest/v1":
        raise SystemExit("unsupported archive manifest schema")
    if not COMMIT.fullmatch(data["repository_commit"]):
        raise SystemExit("repository_commit is not a full Git commit hash")
    if set(data["archive"]) != {"filename", "sha256"}:
        raise SystemExit("archive fields do not match schema v1")
    if not SHA256.fullmatch(data["archive"]["sha256"]):
        raise SystemExit("archive sha256 is not a lowercase SHA-256 digest")

    subprocess.run(
        ["git", "cat-file", "-e", f"{data['repository_commit']}^{{commit}}"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    reproducibility = (ROOT / "docs" / "reproducibility.md").read_text(encoding="utf-8")
    for label, value, documents in (
        ("version", data["version"], (citation, readme, reproducibility)),
        ("version DOI", data["version_doi"], (citation, readme, reproducibility)),
        ("concept DOI", data["concept_doi"], (readme, reproducibility)),
        ("repository commit", data["repository_commit"], (readme, reproducibility)),
        ("archive filename", data["archive"]["filename"], (reproducibility,)),
        ("archive SHA-256", data["archive"]["sha256"], (reproducibility,)),
    ):
        if any(value not in document for document in documents):
            raise SystemExit(f"{label} is inconsistent across archive metadata")

    print(
        "Archive manifest passed: schema v1, commit exists, "
        "and citation/README/reproducibility metadata agree"
    )


if __name__ == "__main__":
    main()
