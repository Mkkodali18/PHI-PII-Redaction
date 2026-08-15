import streamlit as st
import pandas as pd
import plotly.express as px
import time

from regex_patterns import (
    EMAIL_PATTERN,
    PHONE_PATTERN,
    DOB_PATTERN,
    AADHAAR_PATTERN,
)

from utils import find_matches
from spacy_detector import detect_entities
from redactor import redact_text


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="PHI / PII Redaction Pipeline",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background: #F5F7FA;
}

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

section[data-testid="stSidebar"] {
    background: #0F172A;
}

section[data-testid="stSidebar"] * {
    color: white;
}

.header-box {
    background: linear-gradient(90deg, #2563EB, #0EA5E9);
    padding: 25px;
    border-radius: 15px;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🛡️ PHI / PII Redaction")

    st.markdown("---")

    st.subheader("📌 Project Information")

    st.write("**Developer:** Kodali Mohana Krishna")
    st.write("**Version:** 4.0")
    st.write("**Detection Engine:** Regex + spaCy")
    st.write("**Framework:** Streamlit")

    st.markdown("---")

    st.subheader("📊 Features")

    st.markdown("""
    ✅ Email Detection

    ✅ Phone Detection

    ✅ Person Detection

    ✅ Organization Detection

    ✅ DOB Detection

    ✅ Aadhaar Detection

    ✅ Automatic Redaction

    ✅ Analytics Dashboard

    ✅ Download Redacted Record
    """)

    st.markdown("---")

    st.success("🟢 System Status: Ready")

    st.markdown("---")

    st.info(
        """
        Healthcare Data Privacy System

        Protecting Sensitive Patient Information
        """
    )


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="header-box">

<h1>🛡️ PHI / PII Redaction Pipeline</h1>

<h4>Healthcare Data Privacy Dashboard</h4>

Automatically detect and redact sensitive patient information
using Regex and spaCy NLP.

</div>
""", unsafe_allow_html=True)

st.write("")


# ============================================================
# FILE UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "📂 Upload Patient Record (.txt)",
    type=["txt"]
)


# ============================================================
# FILE PROCESSING
# ============================================================

if uploaded_file is not None:

    # Processing status
    st.info("🔄 Processing uploaded patient record...")

    # Start processing timer
    start_time = time.time()

    # --------------------------------------------------------
    # FILE INFORMATION
    # --------------------------------------------------------

    st.success("✅ File uploaded successfully!")

    st.write("**File Name:**", uploaded_file.name)
    st.write("**File Type:**", uploaded_file.type)
    st.write(
        "**File Size:**",
        round(uploaded_file.size / 1024, 2),
        "KB"
    )

    # --------------------------------------------------------
    # READ FILE
    # --------------------------------------------------------

    try:

        text = uploaded_file.read().decode("utf-8")

    except UnicodeDecodeError:

        st.error(
            "❌ Unable to read this file. "
            "Please upload a UTF-8 encoded TXT file."
        )

        st.stop()

    # Empty file validation
    if not text.strip():

        st.error("❌ The uploaded file is empty.")

        st.stop()

    st.success("✅ Patient record loaded successfully")


    # ========================================================
    # REGEX DETECTION
    # ========================================================

    emails = find_matches(
        EMAIL_PATTERN,
        text
    )

    phones = find_matches(
        PHONE_PATTERN,
        text
    )

    dates = find_matches(
        DOB_PATTERN,
        text
    )

    aadhaar = find_matches(
        AADHAAR_PATTERN,
        text
    )


    # ========================================================
    # SPACY DETECTION
    # ========================================================

    persons, locations, organizations = detect_entities(text)


    # ========================================================
    # REDACTION
    # ========================================================

    redacted_text = redact_text(text)


    # ========================================================
    # TOTAL DETECTIONS
    # ========================================================

    total_detected = (
        len(emails)
        + len(phones)
        + len(dates)
        + len(aadhaar)
        + len(persons)
        + len(locations)
        + len(organizations)
    )


    # ========================================================
    # PROCESSING TIME
    # ========================================================

    end_time = time.time()

    processing_time = end_time - start_time


    # ========================================================
    # DETECTION SUMMARY
    # ========================================================

    st.markdown("---")

    st.subheader("📊 Detection Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "📧 Emails",
        len(emails)
    )

    c2.metric(
        "📱 Phones",
        len(phones)
    )

    c3.metric(
        "👤 Persons",
        len(persons)
    )

    c4.metric(
        "🏥 Organizations",
        len(organizations)
    )

    c5, c6, c7 = st.columns(3)

    c5.metric(
        "📅 DOB",
        len(dates)
    )

    c6.metric(
        "🪪 Aadhaar",
        len(aadhaar)
    )

    c7.metric(
        "📈 Total PHI",
        total_detected
    )

    st.info(
        f"🔍 Total PHI/PII Detected: {total_detected}"
    )

    st.info(
        f"⏱️ Processing Time: {processing_time:.2f} seconds"
    )


    # ========================================================
    # ORIGINAL VS REDACTED RECORD
    # ========================================================

    st.markdown("---")

    st.subheader("📄 Patient Record Preview")

    left, right = st.columns(2)

    with left:

        st.markdown(
            "### 📄 Original Patient Record"
        )

        st.text_area(
            label="Original",
            value=text,
            height=350
        )

    with right:

        st.markdown(
            "### 🛡️ Redacted Patient Record"
        )

        st.text_area(
            label="Redacted",
            value=redacted_text,
            height=350
        )


    # ========================================================
    # DOWNLOAD REDACTED RECORD
    # ========================================================

    st.markdown("")

    st.download_button(
        label="⬇️ Download Redacted Patient Record",
        data=redacted_text,
        file_name="redacted_patient_record.txt",
        mime="text/plain"
    )


    # ========================================================
    # DETECTION DETAILS
    # ========================================================

    st.markdown("---")

    st.subheader(
        "🔍 PHI / PII Detection Details"
    )

    col1, col2 = st.columns(2)


    # --------------------------------------------------------
    # LEFT COLUMN
    # --------------------------------------------------------

    with col1:

        with st.expander(
            "📧 Email Addresses",
            expanded=True
        ):

            if emails:

                for item in emails:
                    st.success(item)

            else:

                st.info("No Emails Found")


        with st.expander(
            "📱 Phone Numbers",
            expanded=True
        ):

            if phones:

                for item in phones:
                    st.success(item)

            else:

                st.info("No Phone Numbers Found")


        with st.expander(
            "📅 Dates of Birth",
            expanded=False
        ):

            if dates:

                for item in dates:
                    st.success(item)

            else:

                st.info("No DOB Found")


        with st.expander(
            "🪪 Aadhaar Numbers",
            expanded=False
        ):

            if aadhaar:

                for item in aadhaar:
                    st.success(item)

            else:

                st.info("No Aadhaar Found")


    # --------------------------------------------------------
    # RIGHT COLUMN
    # --------------------------------------------------------

    with col2:

        with st.expander(
            "👤 Person Names",
            expanded=True
        ):

            if persons:

                for item in persons:
                    st.success(item)

            else:

                st.info("No Person Found")


        with st.expander(
            "📍 Locations",
            expanded=True
        ):

            if locations:

                for item in locations:
                    st.success(item)

            else:

                st.info("No Location Found")


        with st.expander(
            "🏥 Organizations",
            expanded=True
        ):

            if organizations:

                for item in organizations:
                    st.success(item)

            else:

                st.info("No Organization Found")


    # ========================================================
    # ANALYTICS DASHBOARD
    # ========================================================

    st.markdown("---")

    st.subheader(
        "📊 Analytics Dashboard"
    )

    chart_data = pd.DataFrame({

        "Category": [
            "Emails",
            "Phones",
            "DOB",
            "Aadhaar",
            "Persons",
            "Locations",
            "Organizations"
        ],

        "Count": [
            len(emails),
            len(phones),
            len(dates),
            len(aadhaar),
            len(persons),
            len(locations),
            len(organizations)
        ]

    })


    left_chart, right_chart = st.columns(2)


    # --------------------------------------------------------
    # PIE CHART
    # --------------------------------------------------------

    with left_chart:

        pie = px.pie(
            chart_data,
            values="Count",
            names="Category",
            hole=0.45,
            title="PHI / PII Distribution"
        )

        pie.update_layout(
            height=450,
            legend_title="Detected Entities"
        )

        st.plotly_chart(
            pie,
            use_container_width=True
        )


    # --------------------------------------------------------
    # BAR CHART
    # --------------------------------------------------------

    with right_chart:

        bar = px.bar(
            chart_data,
            x="Category",
            y="Count",
            text="Count",
            title="Detection Statistics"
        )

        bar.update_traces(
            textposition="outside"
        )

        bar.update_layout(
            height=450,
            xaxis_title="Entity Type",
            yaxis_title="Count"
        )

        st.plotly_chart(
            bar,
            use_container_width=True
        )


    # ========================================================
    # PROJECT STATISTICS
    # ========================================================

    st.markdown("---")

    st.subheader(
        "📈 Overall Statistics"
    )

    a, b, c = st.columns(3)


    with a:

        st.metric(
            "Characters Analysed",
            len(text)
        )


    with b:

        st.metric(
            "Total PHI / PII",
            total_detected
        )


    with c:

        if total_detected > 0:

            st.metric(
                "Privacy Status",
                "Sensitive"
            )

        else:

            st.metric(
                "Privacy Status",
                "Safe"
            )


    # ========================================================
    # DETECTION TABLE
    # ========================================================

    st.markdown("---")

    st.subheader(
        "📋 Detection Summary Table"
    )

    table = pd.DataFrame({

        "Entity": [
            "Emails",
            "Phone Numbers",
            "DOB",
            "Aadhaar",
            "Persons",
            "Locations",
            "Organizations"
        ],

        "Detected": [
            len(emails),
            len(phones),
            len(dates),
            len(aadhaar),
            len(persons),
            len(locations),
            len(organizations)
        ]

    })


    st.dataframe(
        table,
        use_container_width=True
    )


    # ========================================================
    # FINAL DOWNLOAD
    # ========================================================

    st.markdown("---")

    st.download_button(
        label="⬇️ Download Redacted Record",
        data=redacted_text,
        file_name="redacted_patient_record.txt",
        mime="text/plain"
    )


    # ========================================================
    # COMPLETION MESSAGE
    # ========================================================

    st.markdown("---")

    st.success(
        "✅ Analysis Completed Successfully!"
    )