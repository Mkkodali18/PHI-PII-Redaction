from regex_patterns import (
    EMAIL_PATTERN,
    PHONE_PATTERN,
    DOB_PATTERN,
    AADHAAR_PATTERN,
)

from utils import find_matches
from spacy_detector import detect_entities

# Read patient file
with open("sample_data/patient1.txt", "r", encoding="utf-8") as file:
    text = file.read()

print("=" * 50)
print("PHI / PII DETECTION REPORT")
print("=" * 50)

# Regex Detection
emails = find_matches(EMAIL_PATTERN, text)
phones = find_matches(PHONE_PATTERN, text)
dates = find_matches(DOB_PATTERN, text)
aadhaar = find_matches(AADHAAR_PATTERN, text)

# spaCy Detection
persons, locations, organizations = detect_entities(text)

print("\nEmails Found:")
print(emails if emails else "None")

print("\nPhone Numbers Found:")
print(phones if phones else "None")

print("\nDates Found:")
print(dates if dates else "None")

print("\nAadhaar Numbers Found:")
print(aadhaar if aadhaar else "None")

print("\n" + "=" * 50)
print("PERSON NAMES")
print("=" * 50)

if persons:
    for person in persons:
        print(person)
else:
    print("No Person Found")

print("\n" + "=" * 50)
print("LOCATIONS")
print("=" * 50)

if locations:
    for location in locations:
        print(location)
else:
    print("No Location Found")

print("\n" + "=" * 50)
print("ORGANIZATIONS")
print("=" * 50)

if organizations:
    for org in organizations:
        print(org)
else:
    print("No Organization Found")

print("\nDetection Completed Successfully!")