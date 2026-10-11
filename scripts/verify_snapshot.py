"""Verify snapshot integrity and Python syntax without importing parent services."""
import ast
import hashlib
import json
from pathlib import Path


def verify():
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "source-manifest.json").read_text(encoding="utf-8"))
    for record in manifest["files"]:
        path = (root / record["path"]).resolve()
        if not path.is_relative_to(root):
            raise ValueError("Snapshot path escapes the repository")
        content = path.read_bytes()
        if hashlib.sha256(content).hexdigest() != record["sha256"]:
            raise ValueError(f"Snapshot changed: {record['path']}")
        if path.suffix == ".py":
            ast.parse(content, filename=record["path"])
    print(f"Verified {len(manifest['files'])} source hashes and Python syntax.")


if __name__ == "__main__":
    verify()
