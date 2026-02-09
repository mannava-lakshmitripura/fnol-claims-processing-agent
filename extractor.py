import pdfplumber
import re

MANDATORY_FIELDS = [
    "policy_number",
    "policyholder_name",
    "incident_date",
    "incident_location",
    "claim_type",
    "estimated_damage"
]

def extract_text(file_path):
    try:
        if file_path.lower().endswith(".txt"):
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read().lower()

        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += (page.extract_text() or "") + "\n"

        return text.lower()

    except Exception as e:
        print(f"Text extraction failed for {file_path}: {e}")
        return ""


def extract_fields(file_path):
    text = extract_text(file_path)

    extracted = {
        "policy_number": match(text, r"policy number[:\s]*([a-z0-9\-]+)"),
        "policyholder_name": match(text, r"policyholder name[:\s]*([a-z\s]+)"),
        "incident_date": match(text, r"incident date[:\s]*([0-9\/\-]+)"),
        "incident_time": match(text, r"incident time[:\s]*([0-9:apm\s]+)"),
        "incident_location": match(text, r"location[:\s]*([a-z\s]+)"),
        "description": (match(text, r"description[:\s]*([\s\S]+)") or "")[:300],
        "estimated_damage": extract_amount(text),
        "claim_type": match(text, r"claim type[:\s]*([a-z]+)")
    }

    missing = [f for f in MANDATORY_FIELDS if not extracted.get(f)]

    return extracted, missing


def match(text, pattern):
    m = re.search(pattern, text)
    return m.group(1).strip() if m else None


def extract_amount(text):
    m = re.search(r"estimated damage[:\s]*\$?\s?([0-9,]+)", text)
    return int(m.group(1).replace(",", "")) if m else None
