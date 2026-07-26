import re
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")


def detect_entities(text):

    doc = nlp(text)

    persons = set()
    locations = set()
    organizations = set()

    # -----------------------------
    # Ignore incorrect detections
    # -----------------------------
    ignore_persons = {
        "Age",
        "Gender",
        "Phone",
        "Email",
        "Address",
        "Patient",
        "Doctor",
        "Hospital",
        "Prescription",
        "Diagnosis",
        "Symptoms",
        "Date",
        "Name",
        "DOB",
        "Mobile"
    }

    # -----------------------------
    # spaCy Detection
    # -----------------------------
    for ent in doc.ents:

        value = ent.text.strip()

        if ent.label_ == "PERSON":

            if value not in ignore_persons and len(value) > 2:
                persons.add(value)

        elif ent.label_ in ("GPE", "LOC"):

            locations.add(value)

        elif ent.label_ == "ORG":

            organizations.add(value)

    # -----------------------------
    # Custom Rule 1
    # Name:
    # -----------------------------
    name_match = re.search(
        r"Name\s*:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
        text
    )

    if name_match:
        persons.add(name_match.group(1).strip())

    # -----------------------------
    # Custom Rule 2
    # Doctor:
    # -----------------------------
    doctor_match = re.search(
        r"Doctor\s*:\s*(Dr\.?\s*[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)",
        text
    )

    if doctor_match:
        persons.add(doctor_match.group(1).strip())

    # -----------------------------
    # Custom Rule 3
    # Hospital:
    # -----------------------------
    hospital_match = re.search(
        r"Hospital\s*:\s*(.+)",
        text
    )

    if hospital_match:
        organizations.add(
            hospital_match.group(1).strip()
        )

    # -----------------------------
    # Custom Rule 4
    # City / State
    # -----------------------------
    address_match = re.search(
        r"Address\s*:\s*(.+)",
        text
    )

    if address_match:

        address = address_match.group(1)

        for part in address.split(","):

            part = part.strip()

            if len(part) > 2:
                locations.add(part)

    return (
        sorted(persons),
        sorted(locations),
        sorted(organizations)
    )