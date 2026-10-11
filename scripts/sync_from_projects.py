"""Export an explicit Iacon source snapshot from its integrated parent projects.

Only committed, allowlisted source is exported. No vault, environment, logs,
database, credentials or unrelated working-tree changes are read or copied.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def git(checkout, *args):
    return subprocess.check_output(["git", "-C", str(checkout), *args])


def sync(speda, hisar):
    destination = Path(__file__).resolve().parents[1]
    specifications = {
        "speda": (speda, "https://github.com/spedatox/speda-mark6", {
            **{f"packages/igor/app/services/{name}.py": f"src/igor/app/services/{name}.py" for name in
               ("library", "library_indexer", "library_controls", "library_extract", "library_ocr",
                "library_embeddings", "hisar_library_client", "lexical")},
            "packages/igor/app/models/library.py": "src/igor/app/models/library.py",
            "packages/igor/app/schemas/library.py": "src/igor/app/schemas/library.py",
            "packages/igor/app/routers/library.py": "src/igor/app/routers/library.py",
            "packages/igor/app/skills/library.py": "src/igor/app/skills/library.py",
            "packages/igor/app/prompts/core/08_memory.md": "integration/agent-memory-protocol.md",
            "packages/igor/scripts/verify_iacon.py": "verification/verify_iacon.py",
            "packages/igor/scripts/n8n/iacon_reconcile.json": "integration/n8n/iacon_reconcile.json",
            "packages/igor/tests/test_library_hall_records.py": "verification/test_library_hall_records.py",
            "docs/IACON_HALL_OF_RECORDS.md": "docs/INTEGRATION.md",
            "LICENSE": "licenses/SPEDA-AGPL-3.0.txt",
            "logos/svg/optimus-glass.svg": "assets/optimus-glass.svg",
        }),
        "hisar": (hisar, "https://github.com/spedatox/hisar", {
            **{f"server/{name}.py": f"src/hisar/server/{name}.py" for name in
               ("library", "library_models", "library_routes", "library_delivery")},
            "HallOfRecords.jsx": "src/hisar/HallOfRecords.jsx",
            "IaconSettings.jsx": "src/hisar/IaconSettings.jsx",
            "iacon.css": "src/hisar/iacon.css",
            "public/optimus.svg": "src/hisar/public/optimus.svg",
            "tests/test_library.py": "verification/hisar/test_library.py",
        }),
    }
    manifest = {"format": 1, "projects": {}, "files": []}
    for project, (checkout, url, files) in specifications.items():
        revision = git(checkout, "rev-parse", "HEAD").decode().strip()
        manifest["projects"][project] = {"repository": url, "commit": revision}
        for original, target in files.items():
            content = git(checkout, "show", f"{revision}:{original}")
            output = destination / target
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(content)
            manifest["files"].append({"path": target, "project": project, "original_path": original,
                                      "sha256": hashlib.sha256(content).hexdigest()})
    (destination / "source-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Exported {len(manifest['files'])} committed source files.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--speda", type=Path, required=True)
    parser.add_argument("--hisar", type=Path, required=True)
    args = parser.parse_args()
    sync(args.speda.resolve(), args.hisar.resolve())
