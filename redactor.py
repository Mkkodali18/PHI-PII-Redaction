import re

from regex_patterns import (
    EMAIL_PATTERN,
    PHONE_PATTERN,
    DOB_PATTERN,
    AADHAAR_PATTERN,
)

from spacy_detector import detect_entities


def redact_text(text):
    """
    Automatically redact PHI / PII information.
    """

    # -------------------------
    # Regex Redaction
    # -------------------------

    text = re.sub(
        EMAIL_PATTERN,
        "[EMAIL]",
        text
    )

    text = re.sub(
        PHONE_PATTERN,
        "[PHONE]",
        text
    )

    text = re.sub(
        DOB_PATTERN,
        "[DOB]",
        text
    )

    text = re.sub(
        AADHAAR_PATTERN,
        "[AADHAAR]",
        text
    )

    # -------------------------
    # spaCy Entity Redaction
    # -------------------------

    persons, locations, organizations = detect_entities(text)

    # Replace person names
    for person in sorted(persons, key=len, reverse=True):
        text = text.replace(
            person,
            "[PERSON]"
        )

    # Replace locations
    for location in sorted(locations, key=len, reverse=True):
        text = text.replace(
            location,
            "[LOCATION]"
        )

    # Replace organizations
    for org in sorted(organizations, key=len, reverse=True):
        text = text.replace(
            org,
            "[ORGANIZATION]"
        )

    return text