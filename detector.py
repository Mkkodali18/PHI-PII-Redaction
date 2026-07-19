from regex_patterns import (
    EMAIL_PATTERN,
    PHONE_PATTERN,
    DOB_PATTERN,
    AADHAAR_PATTERN,
)

from utils import find_matches


# Read patient file
with open("sample_data/patient1.txt", "r", encoding="utf-8") as file:
    text = file.read()


print("=" * 50)
print("PHI / PII DETECTION REPORT")
print("=" * 50)

# Email
emails = find_matches(EMAIL_PATTERN, text)
print("\nEmails Found:")
print(emails if emails else "None")

# Phone
phones = find_matches(PHONE_PATTERN, text)
print("\nPhone Numbers Found:")
print(phones if phones else "None")

# DOB
dates = find_matches(DOB_PATTERN, text)
print("\nDates Found:")
print(dates if dates else "None")

# Aadhaar
aadhaar = find_matches(AADHAAR_PATTERN, text)
print("\nAadhaar Numbers Found:")
print(aadhaar if aadhaar else "None")

print("\nDetection Completed Successfully!")