from pathlib import Path

files = [
    "app.py",
    "scripts/make_big_csv.py",
    "scripts/fix_whitespace.py",
    "src/analysis.py",
    "src/enrichment.py",
    "src/ingest.py",
    "src/sources.py",
    "src/store.py",
    "src/streaming.py",
    "src/validation.py",
    "tests/test_v1_1.py",
]

for f in files:
    path = Path(f)
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    cleaned = [line.rstrip() for line in lines]
    fixed = "\n".join(cleaned) + "\n"
    path.write_text(fixed, encoding="utf-8")
    print(f"fixed {f}")
