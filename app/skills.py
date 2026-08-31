"""Transparent, non-LLM skills dictionary tailored to the supplied resumes."""

import re

SKILL_ALIASES = {
    "machine learning": "Machine Learning",
    "python": "Python",
    "embedded c": "Embedded C",
    "c": "C",
    "c++": "C++",
    "c#": "C#",
    "java": "Java",
    "javascript": "JavaScript",
    "js": "JavaScript",
    "html": "HTML",
    "css": "CSS",
    "matlab simulink": "MATLAB Simulink",
    "simulink": "Simulink",
    "matlab": "MATLAB",
    "dbms": "DBMS",
    "mysql": "MySQL",
    "sql": "SQL",
    "raspberry pi": "Raspberry Pi",
    "arduino": "Arduino",
    "iot systems": "IoT Systems",
    "iot": "IoT",
    "3d image processing": "3D Image Processing",
    "image processing": "Image Processing",
    "data analysis": "Data Analysis",
    "digital electronics": "Digital Electronics",
    "lidar": "LiDAR",
    "excel": "MS Excel",
    "ms excel": "MS Excel",
    "word": "MS Word",
    "ms word": "MS Word",
    "powerpoint": "MS PowerPoint",
    "ms powerpoint": "MS PowerPoint",
    "thinkspeak": "ThinkSpeak",
    "thinkspreak": "ThinkSpeak",
}

ALIASES = sorted(SKILL_ALIASES.items(), key=lambda x: len(x[0]), reverse=True)


def get_section(text: str, names: list[str]) -> str:
    lines = text.splitlines()
    heading = re.compile(
        r"^\s*(?:" + "|".join(re.escape(n) for n in names) + r")\s*:?\s*$", re.I
    )
    stops = re.compile(
        r"^\s*(education|career objective|professional summary|summary|"
        r"experience|work experience|employment|internship|academic projects|"
        r"projects|certifications?(?: & extracurricular)?|sports experience|"
        r"sports & esports interest|sports achievements & training|"
        r"key strengths|achievements?|interests?)\s*:?\s*$", re.I
    )

    for i, line in enumerate(lines):
        stripped = line.strip()
        match = heading.match(stripped)
        if match:
            end = len(lines)
            for j in range(i + 1, len(lines)):
                if stops.match(lines[j].strip()):
                    end = j
                    break
            return "\n".join(lines[i + 1:end])
        # Some PDF extraction/layouts put the heading and its first content
        # on the same visual line.
        inline = re.match(
            r"^\s*(?:" + "|".join(re.escape(n) for n in names) + r")\s*:?\s+(.+)$",
            stripped, re.I
        )
        if inline:
            end = len(lines)
            for j in range(i + 1, len(lines)):
                if stops.match(lines[j].strip()):
                    end = j
                    break
            return inline.group(1) + "\n" + "\n".join(lines[i + 1:end])
    return ""


def extract_skills(text: str) -> list[str]:
    # The supplied resumes both contain a "TECHNICAL SKILLS" block, but PDF text
    # extraction can sometimes alter the heading/line boundaries. First locate
    # everything after that heading, then fall back to the dedicated section helper.
    match = re.search(r"technical skills\b(.*)$", text, re.I | re.S)
    if match:
        source = match.group(1)
    else:
        section = get_section(text, [
            "technical skills", "technical skills & competencies",
            "skills", "core competencies"
        ])
        source = section if section.strip() else text

    found = []
    for alias, canonical in ALIASES:
        if alias == "js":
            pattern = r"(?<![\w.])js(?![\w.])"
        elif alias in {"c++", "c#"}:
            pattern = rf"(?<!\w){re.escape(alias)}(?!\w)"
        else:
            pattern = rf"(?<!\w){re.escape(alias)}(?!\w)"
        if re.search(pattern, source, re.I) and canonical not in found:
            found.append(canonical)
    return found
