"""Read-only R31 snapshot and evidence-receipt integrity check (not a proof check)."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = "research/goal_a/RECOVERY_SNAPSHOT_2026-10-27_R31.json"
# These are the only snapshot entries changed by the 2026-10-28 navigation update.
# Receipt sources are always checked, even when also present in this set.
NAVIGATION = frozenset({
    "RESULTS.md", "ROADMAP.md", "STATUS.md",
    "checks/update_navigation.py", "research/goal_a/README.md",
})


def check(root, allow_navigation=False):
    root = root.resolve()
    snapshot_path = root / SNAPSHOT
    data = json.loads(snapshot_path.read_text(encoding="utf-8"))
    errors, changed = [], []

    def matches(path, expected):
        path = path.resolve()
        if not path.is_relative_to(root) or not path.is_file():
            return False
        return hashlib.sha256(path.read_bytes()).hexdigest() == expected

    for name, expected in data["file_sha256"].items():
        if matches(root / name, expected):
            continue
        if allow_navigation and name in NAVIGATION and (root / name).is_file():
            changed.append(name)
        else:
            errors.append("snapshot mismatch: " + name)

    source_count = 0
    for receipt in data["evidence_integrity"]:
        report = receipt["report"]
        if not matches(snapshot_path.parent / report, receipt["sha256"]):
            errors.append("report mismatch: " + report)
        for name, recorded in receipt["source_checks"].items():
            source_count += 1
            if recorded["actual"] != recorded["expected"]:
                errors.append("inconsistent saved receipt: " + name)
            if not matches(snapshot_path.parent / name, recorded["expected"]):
                errors.append("receipt source mismatch: " + name)
    return data, errors, changed, source_count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-navigation-updates", action="store_true",
                        help="Report five named navigation entries separately; never skip receipt sources.")
    args = parser.parse_args()
    data, errors, changed, source_count = check(ROOT, args.allow_navigation_updates)
    for name in changed:
        print("DOCUMENTATION DIFF (historical hash retained): " + name)
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"PASS: {len(data['file_sha256']) - len(changed)} unchanged snapshot files; "
          f"{len(changed)} declared navigation differences; "
          f"{len(data['evidence_integrity'])} reports and {source_count} source receipts")
    print("Integrity only; does not certify mathematical claims or completion of Goal A.")


if __name__ == "__main__":
    main()
