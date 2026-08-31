# Architecture

```text
                 ┌──────────────────────┐
                 │      PDF / DOCX      │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │    Document Parser   │
                 │      parser.py       │
                 └──────────┬───────────┘
                            │ raw text
                            ▼
                 ┌──────────────────────┐
                 │  Text Normalization  │
                 │   extractor.py       │
                 └──────────┬───────────┘
                            │
             ┌──────────────┼──────────────┐
             ▼              ▼              ▼
        Contact Rules   Skills Rules   Section Rules
        Email/Phone     Skill aliases   Education
        LinkedIn/GitHub                 Experience
             └──────────────┬──────────────┘
                            ▼
                 ┌──────────────────────┐
                 │ Structured Python   │
                 │       dict           │
                 └──────────┬───────────┘
                            ▼
                 ┌──────────────────────┐
                 │        JSON          │
                 └──────────────────────┘
```

## Components

### `app/parser.py`
Responsible only for converting PDF/DOCX files into text.

### `app/skills.py`
Contains the editable skill dictionary and section-detection helper.

### `app/extractor.py`
Coordinates extraction and contains deterministic rules for:
- Name
- Email
- Phone
- Education
- Work experience
- LinkedIn
- GitHub

### `main.py`
Command-line interface.

### `streamlit_app.py`
Optional browser interface for uploading a PDF/DOCX and viewing/downloading JSON.

### `tests/`
Contains tests against the supplied PDF and DOCX resumes.
