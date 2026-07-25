import streamlit as st
from regex_patterns import (
    EMAIL_PATTERN,
    PHONE_PATTERN,
    DOB_PATTERN,
    AADHAAR_PATTERN
)
from utils import find_matches
from spacy_detector import detect_entities
from redactor import redact_text

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="PHI / PII Redaction Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# -------------------------------------------------
# Sidebar
# -------------------------------------------------

st.sidebar.title("🛡️ PHI / PII Redaction")

st.sidebar.markdown("---")

st.sidebar.write("Developer")
st.sidebar.success("Kodali Mohana Krishna")

st.sidebar.write("Technology")
st.sidebar.info("Python\nRegex\nspaCy\nStreamlit")

st.sidebar.markdown("---")

st.sidebar.write("Version 1.0")

# -------------------------------------------------
# Title
# -------------------------------------------------

st.title("🛡️ PHI / PII Redaction Pipeline")

st.write(
    "Upload a patient medical record to detect and redact sensitive information."
)

st.markdown("---")

# -------------------------------------------------
# Upload
# -------------------------------------------------

uploaded_file = st.file_uploader(
    "📂 Upload Patient Record",
    type=["txt"]
)

if uploaded_file is not None:

    text = uploaded_file.read().decode("utf-8")

    # ---------------------------------------------
    # Detection
    # ---------------------------------------------

    emails = find_matches(EMAIL_PATTERN, text)

    phones = find_matches(PHONE_PATTERN, text)

    dates = find_matches(DOB_PATTERN, text)

    aadhaar = find_matches(AADHAAR_PATTERN, text)

    persons, locations, organizations = detect_entities(text)

    # ---------------------------------------------
    # Metrics
    # ---------------------------------------------

    st.subheader("📊 Detection Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Emails", len(emails))
    c2.metric("Phones", len(phones))
    c3.metric("Persons", len(persons))
    c4.metric("Organizations", len(organizations))

    st.markdown("---")

    # ---------------------------------------------
    # Original Text
    # ---------------------------------------------

    left, right = st.columns(2)

    with left:

        st.subheader("📄 Original Patient Record")

        st.text_area(
            "Original",
            text,
            height=350
        )

    # ---------------------------------------------
    # Redacted Text
    # ---------------------------------------------

    redacted = redact_text(text)

    with right:

        st.subheader("🛡️ Redacted Patient Record")

        st.text_area(
            "Redacted",
            redacted,
            height=350
        )

    st.markdown("---")

    # ---------------------------------------------
    # Detection Results
    # ---------------------------------------------

    st.subheader("🔍 Detection Results")

    col1, col2 = st.columns(2)

    with col1:

        st.success("📧 Emails")
        st.write(emails)

        st.success("📞 Phone Numbers")
        st.write(phones)

        st.success("📅 Date of Birth")
        st.write(dates)

        st.success("🪪 Aadhaar Numbers")
        st.write(aadhaar)

    with col2:

        st.success("👤 Person Names")
        st.write(persons)

        st.success("📍 Locations")
        st.write(locations)

        st.success("🏥 Organizations")
        st.write(organizations)

    st.markdown("---")

    # ---------------------------------------------
    # Download
    # ---------------------------------------------

    st.download_button(
        label="⬇ Download Redacted File",
        data=redacted,
        file_name="redacted_patient_record.txt",
        mime="text/plain"
    )

else:

    st.info("Please upload a patient record (.txt)")