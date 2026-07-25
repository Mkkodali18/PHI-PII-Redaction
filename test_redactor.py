from redactor import redact_text

with open("sample_data/patient1.txt", "r", encoding="utf-8") as file:
    text = file.read()

print("Original Record")
print("=" * 50)
print(text)

print("\n")

redacted = redact_text(text)

print("Redacted Record")
print("=" * 50)
print(redacted)