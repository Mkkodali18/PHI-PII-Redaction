import streamlit as st
import re
from redactor import redact_text

# ----------------------------------------
# Page Configuration
# ----------------------------------------

st.set_page_config(
    page_title="PHI / PII Redaction Dashboard",
    page_icon="🛡️",
    layout="wide"
)

# ----------------------------------------
# Sidebar
# ----------------------------------------

st.sidebar.title("🛡️ Project Information")

st.sidebar.write("Project : PHI / PII Redaction")

st.sidebar.write("Developer : Kodali Mohana Krishna")

st.sidebar.write("Version : 1.0")

st.sidebar.success("Week 4")

# ----------------------------------------
# Main Title
# ----------------------------------------

st.title("🛡️ PHI / PII Redaction Pipeline")

st.write(
    "Upload a patient record to detect and automatically redact sensitive information."
)

st.divider()

# ----------------------------------------
# Upload
# ----------------------------------------

uploaded_file = st.file_uploader(
    "Upload Patient Record",
    type=["txt"]
)

if uploaded_file is not None:

    text = uploaded_file.read().decode("utf-8")

    # -----------------------------
    # Original Record
    # -----------------------------

    st.subheader("📄 Original Patient Record")

    st.text_area(
        "Original",
        text,
        height=250
    )

    # -----------------------------
    # Regex Detection
    # -----------------------------

    EMAIL_PATTERN = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    PHONE_PATTERN = r"\b[6-9]\d{9}\b"

    DOB_PATTERN = r"\b\d{2}/\d{2}/\d{4}\b"

    AADHAAR_PATTERN = r"\b\d{4}\s\d{4}\s\d{4}\b"

    emails = re.findall(EMAIL_PATTERN, text)

    phones = re.findall(PHONE_PATTERN, text)

    dob = re.findall(DOB_PATTERN, text)

    aadhaar = re.findall(AADHAAR_PATTERN, text)

    # -----------------------------
    # Dashboard Cards
    # -----------------------------

    st.subheader("📊 Detection Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Emails", len(emails))

    c2.metric("Phones", len(phones))

    c3.metric("DOB", len(dob))

    c4.metric("Aadhaar", len(aadhaar))

    st.divider()

    # -----------------------------
    # Detection Results
    # -----------------------------

    st.subheader("🔍 Detection Results")

    st.write("### Emails")
    st.write(emails)

    st.write("### Phone Numbers")
    st.write(phones)

    st.write("### DOB")
    st.write(dob)

    st.write("### Aadhaar")
    st.write(aadhaar)

    st.divider()

    # -----------------------------
    # Redacted Record
    # -----------------------------

    redacted = redact_text(text)

    st.subheader("🛡️ Redacted Patient Record")

    st.text_area(
        "Redacted",
        redacted,
        height=250
    )

    st.download_button(
        "⬇ Download Redacted File",
        redacted,
        file_name="redacted_patient_record.txt",
        mime="text/plain"
    )

else:

    st.info("Please upload a patient record.")