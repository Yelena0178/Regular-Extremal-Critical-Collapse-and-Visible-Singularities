"""Maintain the research file index and current byte manifest (standard library only).

Run from any directory: python checks/update_navigation.py --write or --check.
Uses Git's tracked/non-ignored file list; never changes research evidence files.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
INDEX = "research/goal_a/FILE_INDEX.md"
MANIFEST = "FILE_MANIFEST.json"
DATE = "2026-10-20"


def repository_files():
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=ROOT, check=True, capture_output=True,
    )
    paths = {p.decode("utf-8") for p in result.stdout.split(b"\0") if p}
    paths.update((INDEX, MANIFEST))
    return sorted(p for p in paths if (ROOT / p).is_file() or p == INDEX)


def file_index(paths):
    research = [p for p in paths if p.startswith("research/goal_a/") and p != INDEX]
    categories = [
        ("研究文档与阶段记录", []), ("核验与认证脚本", []),
        ("构造、演化与探索脚本", []), ("JSON 证据与结果", []),
        ("日志、数值数据与运行环境", []),
    ]
    for path in research:
        relative = path.removeprefix("research/goal_a/")
        name = Path(path).name
        if name.endswith(".md"):
            group = 0
        elif name.endswith(".py"):
            group = 1 if name.startswith(("verify_", "certify_", "check_", "validate_")) else 2
        else:
            group = 3 if name.endswith(".json") else 4
        categories[group][1].append((path, relative))
    lines = [
        "# 目标 A 完整文件索引", "",
        "由 `python checks/update_navigation.py --write` 生成；统计 Git 已跟踪及未忽略文件，不含本索引自身。",
        "运行环境缓存、被忽略的检查输出及未纳入版本管理的网页不在此表。", "",
        "先读 [当前进展](README.md) 与 [验收标准](ACCEPTANCE.md)。条目仅定位文件，不代表数学结论已获认证。",
        "JSON、日志及数值文件均保留原文件名和内容；历史记录按文内日期理解。", "",
        f"本目录共列出 **{len(research)}** 个文件。", "",
    ]
    for title, entries in categories:
        lines.extend([f"## {title}（{len(entries)}）", ""])
        for path, relative in entries:
            label = relative
            if path.endswith(".md"):
                heading = next((s[2:].strip() for s in (ROOT / path).read_text(encoding="utf-8-sig").splitlines()
                                if s.startswith("# ")), "")
                label += " — " + heading.replace("[", "(").replace("]", ")") if heading else ""
            lines.append(f"- [{label}]({relative})")
        lines.append("")
    return "\n".join(lines)


def manifest(paths):
    files = []
    for path in paths:
        if path == MANIFEST:
            continue
        data = (ROOT / path).read_bytes()
        files.append({"path": path, "size_bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
    counts = Counter(item["path"].split("/")[0] for item in files if "/" in item["path"])
    return json.dumps({
        "snapshot_date": DATE,
        "scope": "current tracked and non-ignored repository files; excludes itself and ignored generated outputs; bytes only",
        "historical_manifest": "checks/FILE_MANIFEST_2026-10-10.json",
        "directory_file_counts": dict(sorted(counts.items())),
        "files": files,
    }, ensure_ascii=False, indent=2) + "\n"


def save_or_check(path, expected, write):
    target = ROOT / path
    if write:
        target.write_text(expected, encoding="utf-8", newline="\n")
    elif not target.exists() or target.read_text(encoding="utf-8") != expected:
        raise SystemExit(f"OUTDATED: {path}; run python checks/update_navigation.py --write")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    paths = repository_files()
    save_or_check(INDEX, file_index(paths), args.write)
    save_or_check(MANIFEST, manifest(paths), args.write)
    print("PASS: research index and current byte manifest " + ("updated" if args.write else "match repository files"))


if __name__ == "__main__":
    main()
