#!/usr/bin/env python3
"""Stdlib packaging checks and conservative research bookkeeping gate.

This does not prove mathematics, validate arbitrary YAML, or run a language model.
The authored frontmatter deliberately uses only two plain single-line scalars.
"""
import argparse
import copy
import json
import re
import shutil
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

REQUIRED = (
    'SKILL.md', 'README.md', 'references/GOAL-CONTROL.md',
    'references/RESEARCH-METHODOLOGY.md', 'references/PROOF-AUDIT.md',
    'references/EVIDENCE-STANDARDS.md', 'references/RECCVS-PROFILE.md',
    'assets/GOAL-TEMPLATE.md', 'assets/CLAIM-TEMPLATE.md',
    'assets/CHECKPOINT-TEMPLATE.md', 'scripts/validate_skill.py',
)
LOGIC = {'PROVED', 'CONDITIONAL', 'CONJECTURAL', 'OPEN', 'REFUTED'}
EVIDENCE = {'ANALYTIC', 'EXACT_ALGEBRA', 'CERTIFIED_NUMERICS',
            'EXPERIMENTAL', 'LITERATURE', 'HEURISTIC'}
AUDIT = {'UNCHECKED', 'INTERNAL_AUDIT', 'INDEPENDENT_REVIEW', 'FAILED'}
ROLES = {'NECESSARY', 'AUXILIARY', 'SCREEN', 'EXPLORATORY'}


def validate(root):
    root = Path(root).resolve()
    errors = []
    for item in REQUIRED:
        if not (root / item).is_file():
            errors.append(f'missing required file: {item}')
    if not (root / 'SKILL.md').is_file():
        return errors
    try:
        skill = (root / 'SKILL.md').read_text(encoding='utf-8')
        match = re.match(r'\A---\n(.*?)\n---\n', skill, re.S)
        if not match:
            raise ValueError('SKILL.md: missing or malformed frontmatter')
        fields = {}
        for line in match[1].splitlines():
            pair = re.fullmatch(r'(name|description): ([^\n]+)', line)
            if not pair or pair[1] in fields:
                raise ValueError('frontmatter: use unique name/description plain scalar lines')
            value = pair[2]
            if ': ' in value or any(c in value for c in '#{}[]&*!|>\'"`'):
                raise ValueError('frontmatter: unsupported YAML scalar syntax')
            fields[pair[1]] = value
        if set(fields) != {'name', 'description'}:
            raise ValueError('frontmatter requires name and description')
        name = fields['name']
        if (len(name) > 64 or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name)
                or name != root.name):
            raise ValueError('frontmatter name invalid or differs from folder')
        if not 1 <= len(fields['description'].strip()) <= 1024:
            raise ValueError('description must contain 1..1024 characters')
        if not skill[match.end():].strip():
            raise ValueError('SKILL.md has no instructions')
    except (UnicodeError, ValueError) as exc:
        errors.append(str(exc))
    for path in sorted(root.rglob('*')):
        if not path.is_file() or path.suffix not in {'.md', '.py'}:
            continue
        if not path.resolve().is_relative_to(root):
            errors.append(f'file escapes package: {path.name}')
            continue
        try:
            content = path.read_bytes().decode('utf-8')
        except UnicodeError:
            errors.append(f'invalid UTF-8: {path.name}')
            continue
        if content.startswith('\ufeff') or '\x00' in content:
            errors.append(f'BOM or NUL: {path.name}')
        if path.suffix == '.py':
            try:
                compile(content, str(path), 'exec')
            except SyntaxError as exc:
                errors.append(f'Python syntax: {exc}')
            continue
        fence = None
        visible = []
        for line in content.splitlines():
            marker = re.match(r'^\s*(`{3,}|~{3,})(.*)$', line)
            if marker:
                if fence is None:
                    fence = marker[1]
                elif marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                    fence = None
            elif fence is None:
                visible.append(line)
        if fence:
            errors.append(f'unclosed Markdown fence: {path.name}')
        for target in re.findall(r'\[[^\]\n]+\]\(([^)\n]+)\)', '\n'.join(visible)):
            url = urlsplit(target.strip('<>'))
            if url.scheme or url.netloc or not url.path:
                continue
            dest = (path.parent / unquote(url.path)).resolve()
            if not dest.is_relative_to(root):
                errors.append(f'link escapes package: {path.name}: {target}')
            elif not dest.is_file():
                errors.append(f'broken link: {path.name}: {target}')
            # This package uses file links, not section anchors; anchors are not checked.
    return errors


def completion_errors(state):
    """Check a JSON receipt's claims, not the truth of supplied attestations."""
    if not isinstance(state, dict):
        return ['state must be an object']
    errors = []
    for field in ('contract_version', 'next_action'):
        if not isinstance(state.get(field), str) or not state[field].strip():
            errors.append(f'missing {field}')
    claims = state.get('claims')
    required = state.get('required')
    if not isinstance(claims, dict) or not claims or not isinstance(required, list) or not required:
        return errors + ['nonempty claims mapping and required ID list needed']
    visited, active = set(), set()

    def visit(cid):
        if not isinstance(cid, str) or cid not in claims:
            errors.append(f'missing dependency: {cid}')
            return
        if cid in active:
            errors.append(f'cyclic dependency: {cid}')
            return
        if cid in visited:
            return
        active.add(cid)
        c = claims[cid]
        if not isinstance(c, dict):
            errors.append(f'{cid}: claim must be an object')
            active.remove(cid)
            visited.add(cid)
            return
        for field, allowed in [('logic', LOGIC), ('audit', AUDIT), ('role', ROLES)]:
            if not isinstance(c.get(field), str) or c[field] not in allowed:
                errors.append(f'{cid}: invalid {field}')
        if c.get('logic') != 'PROVED':
            errors.append(f'{cid}: unresolved logic')
        if c.get('audit') not in {'INTERNAL_AUDIT', 'INDEPENDENT_REVIEW'}:
            errors.append(f'{cid}: audit not passed')
        ev = c.get('evidence')
        if (not isinstance(ev, list) or not ev or any(not isinstance(e, str) or e not in EVIDENCE for e in ev)
                or set(ev) <= {'EXPERIMENTAL', 'HEURISTIC'}):
            errors.append(f'{cid}: insufficient or invalid evidence')
        for flag in ('premises_discharged', 'external_hypotheses_checked',
                     'scope_covers_claim', 'global_coverage_checked',
                     'no_fatal_defects', 'proof_inspectable'):
            if c.get(flag) is not True:
                errors.append(f'{cid}: {flag} not attested')
        for field in ('statement', 'proof_receipt'):
            if not isinstance(c.get(field), str) or not c[field].strip():
                errors.append(f'{cid}: missing {field}')
        deps = c.get('dependencies')
        if not isinstance(deps, list):
            errors.append(f'{cid}: dependencies must be an explicit list')
        else:
            for dep in deps:
                visit(dep)
        active.remove(cid)
        visited.add(cid)

    for cid in required:
        visit(cid)
        if isinstance(cid, str) and isinstance(claims.get(cid), dict) and claims[cid].get('role') != 'NECESSARY':
            errors.append(f'{cid}: required gate cannot be replaced by screen/exploration')
    return errors


def self_test(root):
    checks = 0
    with tempfile.TemporaryDirectory(prefix='math-skill-test-') as folder:
        clone = Path(folder) / root.name
        shutil.copytree(root, clone, ignore=shutil.ignore_patterns('__pycache__'))
        def reject(path, replacement):
            nonlocal checks
            original = path.read_bytes()
            try:
                path.write_bytes(replacement)
                if not validate(clone):
                    raise RuntimeError(f'negative control accepted: {path.name}')
                checks += 1
            finally:
                path.write_bytes(original)
        manifest = clone / 'SKILL.md'
        data = manifest.read_bytes()
        reject(manifest, data.replace(b'name: math-research-goal-runner', b'name: Wrong_Name'))
        reject(manifest, data.replace(b'description:', b'unknown:'))
        reject(manifest, b'\xef\xbb\xbf' + data)
        reject(manifest, data + b'\n[missing](references/absent.md)\n')
        reject(manifest, data + b'\n[escape](../outside.md)\n')
        reject(manifest, data + b'\n```text\nunclosed\n')
        reject(clone / 'README.md', b'\xff')
        missing = clone / 'assets/CLAIM-TEMPLATE.md'
        original = missing.read_bytes()
        missing.unlink()
        if not validate(clone):
            raise RuntimeError('missing template accepted')
        missing.write_bytes(original)
        checks += 1
    # Synthetic goal: for all real x, x^2 >= 0. This is bookkeeping only.
    claim = dict(statement='For every real x, x*x >= 0', role='NECESSARY',
                 logic='PROVED', evidence=['ANALYTIC'], audit='INTERNAL_AUDIT',
                 dependencies=[], proof_receipt='Real-order square argument; smoke example')
    for flag in ('premises_discharged', 'external_hypotheses_checked',
                 'scope_covers_claim', 'global_coverage_checked',
                 'no_fatal_defects', 'proof_inspectable'):
        claim[flag] = True
    state = dict(contract_version='synthetic-v1', required=['S1'], claims={'S1': claim},
                 next_action='Audit the ordered-field sign split')
    if completion_errors(state):
        raise RuntimeError('valid synthetic bookkeeping rejected')
    checks += 1
    variants = [('logic', 'CONDITIONAL'), ('logic', 'OPEN'), ('logic', 'REFUTED'),
                ('logic', 'CONJECTURAL'), ('audit', 'FAILED'), ('audit', 'UNCHECKED'),
                ('evidence', ['EXPERIMENTAL']), ('evidence', ['HEURISTIC']),
                ('dependencies', ['missing']), ('dependencies', ['S1']),
                ('role', 'SCREEN'), ('proof_receipt', '')]
    variants += [(flag, False) for flag in claim if flag.endswith(('checked', 'discharged', 'claim', 'defects', 'inspectable'))]
    for field, value in variants:
        changed = copy.deepcopy(state)
        changed['claims']['S1'][field] = value
        if not completion_errors(changed):
            raise RuntimeError(f'completion negative control accepted: {field}={value}')
        checks += 1
    changed = copy.deepcopy(state)
    changed['claims']['S1']['dependencies'] = ['L1']
    changed['claims']['L1'] = dict(claim, logic='CONDITIONAL', role='AUXILIARY')
    if not completion_errors(changed):
        raise RuntimeError('conditional transitive premise accepted')
    return checks + 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', nargs='?', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--check-state', type=Path, help='JSON completion receipt; see README')
    args = parser.parse_args()
    try:
        errors = validate(args.path)
        if args.check_state:
            errors += completion_errors(json.loads(args.check_state.read_text(encoding='utf-8')))
        if errors:
            for error in errors:
                print(f'FAIL: {error}')
            return 1
        if args.self_test:
            print(f'PASS: {self_test(args.path.resolve())} isolated controls/scenarios')
        print('PASS: structure, restricted frontmatter, UTF-8, fences, local file links, Python syntax')
        print('LIMIT: no mathematical truth, arbitrary YAML/Markdown, or runtime loading validation')
        return 0
    except (OSError, ValueError, RuntimeError) as exc:
        print(f'FAIL: {exc}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
