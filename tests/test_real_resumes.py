
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.extractor import extract_resume

ROOT = Path(__file__).resolve().parents[1]

def test_sports_pdf_resume():
    r = extract_resume(str(ROOT/"data/Gagantej_RT_Resume.pdf"))
    assert r["name"] == "Gagantej Rt"
    assert r["email"] == "rtgagantej@gmail.com"
    assert "86605" in r["phone"].replace(" ", "")
    assert {"Python", "Java", "C", "Embedded C", "MATLAB", "MS Excel", "MS Word", "MS PowerPoint"} <= set(r["skills"])
    assert any("RNS Institute of Technology" in (x["institution"] or "") for x in r["education"])
    assert any(x["job_title"] == "Team Administrator" and x["company"] == "FIBA" for x in r["work_experience"])
    assert any(x["job_title"] == "Basketball Coach" and x["company"] == "Soundarya School" for x in r["work_experience"])

def test_ats_docx_resume():
    r = extract_resume(str(ROOT/"data/Gagan_Tej_RT_ATS_Resume.docx"))
    assert r["name"] == "Gagan Tej R T"
    assert r["email"] == "rtgagantej@gmail.com"
    assert "86605" in r["phone"].replace(" ", "")
    assert {"Python", "C++", "Java", "HTML", "JavaScript", "MySQL", "DBMS"} <= set(r["skills"])
    assert any("RNS Institute of Technology" in (x["institution"] or "") for x in r["education"])
    assert any(x["job_title"] == "Engineering Intern" and "Flight Test Centre" in (x["company"] or "") for x in r["work_experience"])
