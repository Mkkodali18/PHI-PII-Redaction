import re

# Email
EMAIL_PATTERN = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

# Indian Phone Number (10 digits)
PHONE_PATTERN = r'\b[6-9]\d{9}\b'

# Date (DD/MM/YYYY or DD-MM-YYYY)
DOB_PATTERN = r'\b\d{2}[/-]\d{2}[/-]\d{4}\b'

# Aadhaar Number
AADHAAR_PATTERN = r'\b\d{4}\s\d{4}\s\d{4}\b'