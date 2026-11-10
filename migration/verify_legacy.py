"""Read-only integrity verification; never runs simulations or writes release files."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = 'ab78e6c64afb6fd487e40a48fbbcd1b09a84ee3fbc9085530f8833de3543d7ec'

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def verify():
    errors = []
    source = json.loads((ROOT / 'migration/source-files.json').read_text(encoding='utf-8'))
    for row in source:
        path = ROOT / row['target_path']
        if not path.is_file() or sha(path) != row['sha256'].lower():
            errors.append({'path': row['target_path'], 'reason': 'source hash mismatch or missing'})
    counts = {}
    manifests = (
        ('V1', ROOT, ROOT / '06_reproducibility/release_manifest.csv'),
        ('V2 historical', ROOT / '07_version2_uk_petition', ROOT / '07_version2_uk_petition/06_reproducibility/release_manifest_v2.csv'),
        ('V3 historical', ROOT / '08_version3_response_dashboard', ROOT / '08_version3_response_dashboard/06_reproducibility/release_manifest_v3.csv'),
    )
    for label, base, manifest in manifests:
        count = 0
        with manifest.open(encoding='utf-8-sig', newline='') as stream:
            for row in csv.DictReader(stream):
                relative = row['relative_path']
                # The navigation README changed; its frozen original is retained.
                if label == 'V1' and relative == 'README.md':
                    path = ROOT / 'repository_history/f0d71f9/README.md'
                else:
                    path = base / relative
                if not path.is_file() or sha(path) != row['sha256'].lower() or path.stat().st_size != int(row['bytes']):
                    errors.append({'manifest': label, 'path': relative, 'reason': 'manifest mismatch or missing'})
                count += 1
        counts[label] = count
    expected = {row['target_path'] for row in source}
    trees = [f'{number:02d}_' for number in range(1, 9)]
    actual_research = {p.relative_to(ROOT).as_posix() for folder in ROOT.iterdir()
                       if folder.is_dir() and any(folder.name.startswith(prefix) for prefix in trees)
                       for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    expected_research = {p for p in expected if any(p.startswith(prefix) for prefix in trees)}
    if actual_research != expected_research:
        errors.append({'reason': 'research file roster differs', 'missing': sorted(expected_research-actual_research),
                       'extra': sorted(actual_research-expected_research)})
    core = sha(ROOT / '01_model_core/model.py')
    if core != CORE:
        errors.append({'reason': 'core hash mismatch'})
    return {'status': 'passed' if not errors else 'failed', 'read_only': True,
            'source_files_checked': len(source), 'manifest_entries_checked': counts,
            'core_sha256': core, 'research_files': len(actual_research),
            'root_readme_manifest_mapping': 'repository_history/f0d71f9/README.md',
            'simulations_executed': 0, 'errors': errors}

if __name__ == '__main__':
    result = verify()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(result['status'] != 'passed')
