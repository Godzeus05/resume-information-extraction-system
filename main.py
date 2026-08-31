import argparse
import json
from pathlib import Path
from app.extractor import extract_resume

parser = argparse.ArgumentParser(description="Extract structured information from a PDF or DOCX resume.")
parser.add_argument("resume", help="Path to resume")
parser.add_argument("-o", "--output", help="Optional JSON output path")
args = parser.parse_args()

result = extract_resume(args.resume)

if args.output:
    p = Path(args.output)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"JSON written to: {p}")
else:
    print(json.dumps(result, indent=2, ensure_ascii=False))
