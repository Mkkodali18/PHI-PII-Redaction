import streamlit as st
import pandas as pd
import plotly.express as px

from regex_patterns import (
    EMAIL_PATTERN,
    PHONE_PATTERN,
    DOB_PATTERN,
    AADHAAR_PATTERN,
)

from utils import find_matches
from spacy_detector import detect_entities
from redactor import redact_text


# -------------------------------
# PAGE CONFIG
# -------------------------------

st.set_page_config(
    page_title="PHI / PII Redaction Pipeline",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -------------------------------
# CUSTOM CSS
# -------------------------------

st.markdown("""

<style>

.main{
    background:#F5F7FA;
}

.block-container{
    padding-top:1.5rem;
    padding-bottom:2rem;
}

section[data-testid="stSidebar"]{
    background:#0F172A;
}

section[data-testid="stSidebar"] *{
    color:white;
}

.metric-card{

    background:white;

    padding:20px;

    border-radius:12px;

    border:1px solid #E5E7EB;

    box-shadow:0px 4px 12px rgba(0,0,0,.08);

    text-align:center;

}

.header-box{

    background:linear-gradient(90deg,#2563EB,#0EA5E9);

    padding:25px;

    border-radius:15px;

    color:white;

}

.footer{

    text-align:center;

    color:gray;

    font-size:14px;

}

</style>

""", unsafe_allow_html=True)


# -------------------------------
# SIDEBAR
# -------------------------------

st.sidebar.title("🛡️ PHI / PII")

st.sidebar.markdown("---")

st.sidebar.subheader("Healthcare Privacy")

st.sidebar.success("Developer")
st.sidebar.write("Kodali Mohana Krishna")

st.sidebar.success("Version")
st.sidebar.write("4.0")

st.sidebar.success("Status")
st.sidebar.write("🟢 Active")

st.sidebar.markdown("---")

st.sidebar.subheader("Modules")

st.sidebar.write("✔ Regex Detection")
st.sidebar.write("✔ spaCy NLP")
st.sidebar.write("✔ Automatic Redaction")
st.sidebar.write("✔ Analytics Dashboard")
st.sidebar.write("✔ Download Report")

st.sidebar.markdown("---")

st.sidebar.info(
"""
Healthcare Data Privacy System

Protecting Sensitive Patient Information
"""
)


# -------------------------------
# HEADER
# -------------------------------

st.markdown("""

<div class="header-box">

<h1>🛡️ PHI / PII Redaction Pipeline</h1>

<h4>Healthcare Data Privacy Dashboard</h4>

Automatically detect and redact sensitive patient information using
Regex and spaCy NLP.

</div>

""", unsafe_allow_html=True)

st.write("")

uploaded_file = st.file_uploader(

    "📂 Upload Patient Record (.txt)",

    type=["txt"]

)

if uploaded_file is not None:

    text = uploaded_file.read().decode("utf-8")

    st.success("✅ Patient Record Uploaded Successfully")

        # ============================================
    # REGEX DETECTION
    # ============================================

    emails = find_matches(EMAIL_PATTERN, text)
    phones = find_matches(PHONE_PATTERN, text)
    dates = find_matches(DOB_PATTERN, text)
    aadhaar = find_matches(AADHAAR_PATTERN, text)

    # ============================================
    # SPACY DETECTION
    # ============================================

    persons, locations, organizations = detect_entities(text)

    # ============================================
    # REDACT PATIENT RECORD
    # ============================================

    redacted_text = redact_text(text)

    total_detected = (
        len(emails)
        + len(phones)
        + len(dates)
        + len(aadhaar)
        + len(persons)
        + len(locations)
        + len(organizations)
    )

    st.markdown("---")

    st.subheader("📊 Detection Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("📧 Emails", len(emails))
    c2.metric("📱 Phones", len(phones))
    c3.metric("👤 Persons", len(persons))
    c4.metric("🏥 Organizations", len(organizations))

    c5, c6, c7 = st.columns(3)

    c5.metric("📅 DOB", len(dates))
    c6.metric("🪪 Aadhaar", len(aadhaar))
    c7.metric("📈 Total PHI", total_detected)

    st.markdown("---")

