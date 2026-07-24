import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")


def detect_entities(text):
    """
    Detect PERSON, LOCATION and ORGANIZATION entities.
    """

    doc = nlp(text)

    persons = set()
    locations = set()
    organizations = set()

    ignore_orgs = {
        "Phone",
        "DOB",
        "Email",
        "Address",
        "Patient",
        "Symptoms",
        "Aadhaar",
        "Doctor",
        "Hospital"
    }

    for ent in doc.ents:

        if ent.label_ == "PERSON":
            persons.add(ent.text.strip())

        elif ent.label_ in ("GPE", "LOC"):
            locations.add(ent.text.strip())

        elif ent.label_ == "ORG":
            if ent.text.strip() not in ignore_orgs:
                organizations.add(ent.text.strip())

    return (
        sorted(persons),
        sorted(locations),
        sorted(organizations),
    )