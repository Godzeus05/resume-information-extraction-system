# Resume Information Extraction System

A deterministic, rule-based Python implementation of the internship assignment.

## This version is tailored to the supplied resumes

The project is tested with both:

- `data/Gagantej_RT_Resume.pdf`
- `data/Gagan_Tej_RT_ATS_Resume.docx`

The two resumes use different structures. The parser therefore recognizes section headings such as `PROFESSIONAL SUMMARY`, `CORE COMPETENCIES`, `SPORTS EXPERIENCE`, `EDUCATION`, `TECHNICAL SKILLS`, `CAREER OBJECTIVE`, `INTERNSHIP`, and `ACADEMIC PROJECTS`.

## What it extracts

Mandatory:
- Full name
- Email
- Phone
- Skills

Bonus:
- Education
- Work experience
- LinkedIn
- GitHub

## Technologies

- Python
- pypdf
- python-docx
- Regular expressions
- Rule-based section and entity extraction

**No external LLM or Generative AI API is used for resume extraction.**

## Install

```bash
python -m venv .venv
```

Windows:

```bash
.venv\\Scripts\\activate
```

Then:

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py "data/Gagantej_RT_Resume.pdf"
python main.py "data/Gagan_Tej_RT_ATS_Resume.docx"
```

Save JSON:

```bash
python main.py "data/Gagantej_RT_Resume.pdf" -o output/gagantej.json
```

## Test

```bash
pytest -q
```

The tests validate extraction against both supplied resume formats.

## Design decisions

The parser is deliberately transparent rather than using a black-box model. Skills are identified using a maintained dictionary and aliases. Contact details use regex. Education and experience use recognizable headings and layout rules.

The implementation also handles the two different layouts found in the supplied resumes: the sports resume contains `SPORTS EXPERIENCE`, while the ATS resume contains an `INTERNSHIP` section and structured technical-skill rows.

## Limitations

- Scanned/image-only PDFs are not OCR'd.
- Name extraction is heuristic.
- Skill detection depends on the maintained dictionary.
- Unusual resume layouts may require additional rules.
- Optional information is returned as `null` or `[]` when not present.
- The parser does not infer or invent information.

## Validation

The parser was validated against both supplied files and includes automated tests for each format. It handles the different headings and layouts present in the two resumes rather than assuming a single resume template.
