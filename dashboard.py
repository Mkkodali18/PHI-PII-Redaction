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

    # ============================================
    # ORIGINAL VS REDACTED RECORD
    # ============================================

    st.subheader("📄 Patient Record Preview")

    left, right = st.columns(2)

    with left:

        st.markdown("### 📄 Original Patient Record")

        st.text_area(
            label="Original",
            value=text,
            height=350
        )

    with right:

        st.markdown("### 🛡️ Redacted Patient Record")

        st.text_area(
            label="Redacted",
            value=redacted_text,
            height=350
        )

    st.markdown("")

    st.download_button(
        label="⬇ Download Redacted Patient Record",
        data=redacted_text,
        file_name="redacted_patient_record.txt",
        mime="text/plain"
    )

    st.markdown("---")

    # ============================================
    # DETECTION DETAILS
    # ============================================

    st.subheader("🔍 PHI / PII Detection Details")

    col1, col2 = st.columns(2)

    with col1:

        with st.expander("📧 Email Addresses", expanded=True):

            if emails:
                for item in emails:
                    st.success(item)
            else:
                st.info("No Emails Found")

        with st.expander("📱 Phone Numbers", expanded=True):

            if phones:
                for item in phones:
                    st.success(item)
            else:
                st.info("No Phone Numbers Found")

        with st.expander("📅 Dates of Birth", expanded=False):

            if dates:
                for item in dates:
                    st.success(item)
            else:
                st.info("No DOB Found")

        with st.expander("🪪 Aadhaar Numbers", expanded=False):

            if aadhaar:
                for item in aadhaar:
                    st.success(item)
            else:
                st.info("No Aadhaar Found")

    with col2:

        with st.expander("👤 Person Names", expanded=True):

            if persons:
                for item in persons:
                    st.success(item)
            else:
                st.info("No Person Found")

        with st.expander("📍 Locations", expanded=True):

            if locations:
                for item in locations:
                    st.success(item)
            else:
                st.info("No Location Found")

        with st.expander("🏥 Organizations", expanded=True):

            if organizations:
                for item in organizations:
                    st.success(item)
            else:
                st.info("No Organization Found")

    st.markdown("---")

        # ============================================
    # ANALYTICS DASHBOARD
    # ============================================

    st.subheader("📊 Analytics Dashboard")

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

    st.markdown("---")

    # ============================================
    # PROJECT STATISTICS
    # ============================================

    st.subheader("📈 Overall Statistics")

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

    st.markdown("---")

    # ============================================
    # DETECTION TABLE
    # ============================================

    st.subheader("📋 Detection Summary Table")

    table = pd.DataFrame({

        "Entity":[
            "Emails",
            "Phone Numbers",
            "DOB",
            "Aadhaar",
            "Persons",
            "Locations",
            "Organizations"
        ],

        "Detected":[
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

    st.markdown("---")

    # ============================================
    # DOWNLOAD BUTTON
    # ============================================

    st.download_button(

        label="⬇ Download Redacted Record",

        data=redacted_text,

        file_name="redacted_patient_record.txt",

        mime="text/plain"

    )

    st.markdown("---")

    st.success("✅ Analysis Completed Successfully!")

    st.markdown("""

""")

