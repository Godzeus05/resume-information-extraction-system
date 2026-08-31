
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.extractor import extract_resume


ROOT = Path(__file__).resolve().parents[1]


def test_required_keys_and_types():
    result = extract_resume(str(ROOT / "data" / "Gagan_Tej_RT_ATS_Resume.docx"))

    assert {"name", "email", "phone", "skills"} <= result.keys()
    assert isinstance(result["name"], str)
    assert isinstance(result["email"], str)
    assert isinstance(result["phone"], str)
    assert isinstance(result["skills"], list)
    assert isinstance(result["education"], list)
    assert isinstance(result["work_experience"], list)


def test_supported_extensions():
    pdf_result = extract_resume(str(ROOT / "data" / "Gagantej_RT_Resume.pdf"))
    docx_result = extract_resume(str(ROOT / "data" / "Gagan_Tej_RT_ATS_Resume.docx"))

    assert pdf_result["email"] == "rtgagantej@gmail.com"
    assert docx_result["email"] == "rtgagantej@gmail.com"
