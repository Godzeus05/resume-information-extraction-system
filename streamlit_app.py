"""Simple web UI for the Resume Information Extraction System."""

import json
import tempfile
from pathlib import Path

import streamlit as st

from app.extractor import extract_resume


st.set_page_config(
    page_title="Resume Information Extractor",
    page_icon="📄",
    layout="centered",
)

st.title("Resume Information Extraction System")
st.caption("Rule-based PDF/DOCX extraction — no external LLM/API used.")

uploaded = st.file_uploader(
    "Upload a resume",
    type=["pdf", "docx"],
    help="Supported formats: PDF and DOCX",
)

if uploaded:
    suffix = Path(uploaded.name).suffix.lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded.getbuffer())
        temp_path = tmp.name

    try:
        with st.spinner("Extracting resume information..."):
            result = extract_resume(temp_path)

        st.success("Extraction complete.")

        st.subheader("Structured JSON")
        st.json(result)

        st.download_button(
            "Download JSON",
            data=json.dumps(result, indent=2, ensure_ascii=False),
            file_name=f"{Path(uploaded.name).stem}.json",
            mime="application/json",
        )
    except Exception as exc:
        st.error(f"Could not process this resume: {exc}")
