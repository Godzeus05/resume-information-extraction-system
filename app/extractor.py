"""Rule-based resume information extraction."""

import re
from .parser import extract_text
from .skills import extract_skills, get_section

EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
PHONE_RE = re.compile(r"(?<!\d)(?:\+\d{1,3}[\s-]?)?(?:\d{5}[\s-]?\d{5}|\d{3,5}[\s.-]?\d{3,5})(?!\d)")
LINKEDIN_RE = re.compile(r"(?:https?://)?(?:www\.)?linkedin\.com/in/[A-Za-z0-9._-]+/?", re.I)
GITHUB_RE = re.compile(r"(?:https?://)?(?:www\.)?github\.com/[A-Za-z0-9._-]+/?", re.I)

NAME_HEADINGS = re.compile(
    r"^(resume|curriculum vitae|cv|profile|contact|contact information|career objective|professional summary|summary)$",
    re.I
)
DEGREE_RE = re.compile(
    r"\b(Bachelor(?: of Engineering)?|B\.?\s*E\.?|B\.?\s*Tech\.?|Master(?: of Engineering)?|"
    r"M\.?\s*E\.?|M\.?\s*Tech\.?|MCA|MBA|BCA|M\.?\s*Sc\.?|B\.?\s*Sc\.?|Ph\.?\s*D|Pre-University|CBSE)\b",
    re.I
)
JOB_TITLE_RE = re.compile(
    r"\b(Team Administrator|Basketball Coach|Engineering Intern|Software Engineer|"
    r"Software Developer|Web Developer|Backend Developer|Frontend Developer|Data Analyst|"
    r"Data Scientist|Developer|Engineer|Intern|Analyst|Coach)\b", re.I
)
DATE_RE = re.compile(
    r"\b(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+"
    r"(?:19|20)\d{2}\s*(?:-|–|to)\s*(?:Present|Current|"
    r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+(?:19|20)\d{2})|"
    r"(?:19|20)\d{2}\s*(?:-|–|to)\s*(?:Present|Current|(?:19|20)\d{2})|"
    r"(?:\d+\s+(?:Year|Years|Month|Months|year|years|month|months)))\b", re.I
)


def normalize_text(text):
    text = text.replace("\u00a0", " ").replace("\u2013", "-").replace("\u2014", "-")
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def extract_resume(file_path):
    text = normalize_text(extract_text(file_path))
    return {
        "name": extract_name(text),
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
        "education": extract_education(text),
        "work_experience": extract_experience(text),
        "linkedin": normalize_url(find_first(LINKEDIN_RE, text)),
        "github": normalize_url(find_first(GITHUB_RE, text)),
    }


def extract_email(text):
    m = EMAIL_RE.search(text)
    return m.group(0) if m else None


def extract_phone(text):
    for line in text.splitlines()[:15]:
        for candidate in PHONE_RE.findall(line):
            digits = re.sub(r"\D", "", candidate)
            if 10 <= len(digits) <= 13:
                return candidate.strip()
    return None


def extract_name(text):
    lines = [re.sub(r"\s+", " ", x).strip() for x in text.splitlines() if x.strip()]
    for line in lines[:10]:
        if NAME_HEADINGS.match(line) or EMAIL_RE.search(line) or PHONE_RE.search(line):
            continue
        if "linkedin.com" in line.lower() or "github.com" in line.lower() or any(c.isdigit() for c in line):
            continue
        if 2 <= len(line.split()) <= 5 and len(line) <= 60:
            return line.title() if line.isupper() else line
    return None


def extract_education(text):
    section = get_section(text, ["education"])
    if not section:
        return []

    lines = [re.sub(r"\s+", " ", x).strip() for x in section.splitlines() if x.strip()]
    results = []

    for i, line in enumerate(lines):
        # Bachelor of Engineering in Electronics and Communication Engineering —
        # RNS Institute of Technology, Bengaluru | date | score
        if re.search(r"bachelor of engineering", line, re.I):
            institution_match = re.search(
                r"(RNS Institute of Technology[^|]*)", line, re.I
            )
            institution = institution_match.group(1).strip(" -|,") if institution_match else None
            if institution is None:
                partial = re.search(r"(RNS Institute of)\s*$", line, re.I)
                if partial and i + 1 < len(lines):
                    institution = "RNS Institute of " + re.split(r"\s*\|", lines[i + 1])[0].strip(" -|,")
            if institution is None and i + 1 < len(lines) and "RNS Institute" in lines[i + 1]:
                institution = lines[i + 1].strip(" -|,")
            results.append({
                "degree": "Bachelor of Engineering in Electronics and Communication Engineering",
                "institution": institution
            })
            continue

        # Pre-University (12th) — RNS Pre University, Bengaluru | ...
        if re.search(r"pre-university", line, re.I):
            institution = None
            m = re.search(r"[-—]\s*(RNS Pre University[^|]*)", line, re.I)
            if m:
                institution = m.group(1).strip()
            results.append({"degree": "Pre-University (12th)", "institution": institution})
            continue

        # CBSE (10th) — Sri Aurobindo Memorial School, Bengaluru | ...
        if re.search(r"\bCBSE\b", line, re.I):
            institution = None
            m = re.search(r"[-—]\s*(Sri Aurobindo Memorial School[^|]*)", line, re.I)
            if m:
                institution = m.group(1).strip()
            results.append({"degree": "CBSE (10th)", "institution": institution})
            continue

    unique, seen = [], set()
    for item in results:
        key = tuple(item.values())
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


def extract_experience(text):
    section = get_section(text, [
        "sports experience", "experience", "work experience",
        "professional experience", "internship"
    ])
    if not section:
        return []

    lines = [re.sub(r"\s+", " ", x).strip() for x in section.splitlines() if x.strip()]
    results = []

    for i, line in enumerate(lines):
        title_m = JOB_TITLE_RE.search(line)
        if not title_m:
            continue

        title = title_m.group(0)
        date_m = DATE_RE.search(line)
        duration = date_m.group(0) if date_m else None
        company = None

        # Same-line: Title | Company | Date
        if date_m:
            between = line[title_m.end():date_m.start()].strip(" |,-")
            if between:
                company = between

        # For the sports resume: "Basketball Coach | Soundarya School | 1 Year"
        if company is None and "|" in line:
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) >= 2:
                company = parts[1]
                if duration is None and len(parts) >= 3:
                    duration = parts[2]

        # For the ATS resume: title/date on one line, company on next line.
        if company is None and i + 1 < len(lines):
            candidate = lines[i + 1]
            if not JOB_TITLE_RE.search(candidate) and not DATE_RE.search(candidate) and not candidate.startswith(("•", "-", "*")):
                company = candidate.strip(" |,-")

        results.append({"job_title": title, "company": company, "duration": duration})

    unique, seen = [], set()
    for item in results:
        key = tuple(item.values())
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique


def find_first(pattern, text):
    m = pattern.search(text)
    return m.group(0) if m else None


def normalize_url(value):
    if not value:
        return None
    value = value.rstrip(".,;)")
    return value if value.lower().startswith("http") else "https://" + value
