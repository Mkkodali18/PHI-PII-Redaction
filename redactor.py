import re

# -----------------------------
# Regex Patterns
# -----------------------------

EMAIL_PATTERN = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

PHONE_PATTERN = r"\b[6-9]\d{9}\b"

DOB_PATTERN = r"\b\d{2}/\d{2}/\d{4}\b"

AADHAAR_PATTERN = r"\b\d{4}\s\d{4}\s\d{4}\b"


# -----------------------------
# Redaction Function
# -----------------------------

def redact_text(text):

    text = re.sub(EMAIL_PATTERN, "[EMAIL REDACTED]", text)

    text = re.sub(PHONE_PATTERN, "[PHONE REDACTED]", text)

    text = re.sub(DOB_PATTERN, "[DOB REDACTED]", text)

    text = re.sub(AADHAAR_PATTERN, "[AADHAAR REDACTED]", text)

    return text