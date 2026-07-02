import re

patterns={

    "Email Address": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}",

    "Phone Number": r"\b[6-9]\d{9}\b",

    "PAN Number": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",

    "Aadhaar Number": r"\b\d{4}\s?\d{4}\s?\d{4}\b",

    "Credit Card": r"\b(?:\d[ -]*?){13,16}\b",

    "Employee ID": r"\b(?:EMP|ID)[-_]?\d+\b",

    "API Key": r"(?:api[_-]?key\s*[:=]\s*[A-Za-z0-9_\-]+)",

    "Password": r"(?:password|pwd)\s*[:=]\s*\S+"
}

def detect_sensitive_data(text):

    detected = {}

    for data_type, pattern in patterns.items():

        matches = re.findall(pattern, text)

        detected[data_type] = matches

    return detected