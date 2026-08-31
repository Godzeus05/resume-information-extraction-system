"""Run extraction on both supplied sample resumes."""
from pathlib import Path
import json
from app.extractor import extract_resume

ROOT = Path(__file__).parent

for path in [
    ROOT / "data" / "Gagantej_RT_Resume.pdf",
    ROOT / "data" / "Gagan_Tej_RT_ATS_Resume.docx",
]:
    print(f"\n=== {path.name} ===")
    print(json.dumps(extract_resume(str(path)), indent=2, ensure_ascii=False))
