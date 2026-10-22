"""Check local file links in current navigation, excluding historical snapshots."""
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = (
    "README.md", "STATUS.md", "RESULTS.md", "ROADMAP.md", "GOAL_A.md",
    "REPRODUCE.md", "VERIFICATION.md", "PROVENANCE.md", "CHANGELOG.md",
    "atlas-map.md", "task-rules.md", "research/README.md", "checks/README.md", "reviews/README.md",
    "research/goal_a/README.md", "research/goal_a/FILE_INDEX.md",
)


def main():
    errors = []
    checked = 0
    for name in DOCUMENTS:
        source = ROOT / name
        content = source.read_text(encoding="utf-8-sig")
        for match in re.finditer(r"\[[^\]\n]+\]\(([^)\n]+)\)", content):
            target = match.group(1).strip().strip("<>")
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path:
                continue
            checked += 1
            path = (source.parent / unquote(url.path)).resolve()
            if not path.is_relative_to(ROOT) or not path.exists():
                line = content.count("\n", 0, match.start()) + 1
                errors.append(f"{name}:{line}: missing or outside repository: {target}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"PASS: {checked} local file links in {len(DOCUMENTS)} current navigation documents")
    print("Historical snapshot links, remote URLs and heading fragments are outside this check.")


if __name__ == "__main__":
    main()
