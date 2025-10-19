import json
import re
from typing import Optional

DATA_PATH = "data/fees.json"  # Path to the fee data file

def load_data(path=DATA_PATH):
    """Loads fee data from the JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

data = load_data()

# Simple keyword mapping for user intent
INTENT_KEYWORDS = {
    "admission_fee": ["admission fee", "admission", "admission fees"],
    "semester_fee": ["semester fee", "tuition", "semester fees"],
    "last_date": ["last date", "due date", "deadline"],
    "late_fine": ["late fine", "late fee", "fine"],
    "installments": ["installment", "installments", "pay in parts"],
    "full_details": ["fee structure", "details", "all info", "full details"]
}

def normalize(text: str) -> str:
    """Converts text to lowercase and removes special characters."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

def detect_course(text: str) -> Optional[str]:
    """Identify the course mentioned in the text (handles dots and spaces)."""
    text_n = normalize(text)
    for course in data.keys():
        course_clean = normalize(course)  # remove dots, lowercase
        if course_clean in text_n:
            return course
    return None


def detect_intent(text: str):
    """Identify the type of question asked."""
    text_n = normalize(text)
    for intent, kwlist in INTENT_KEYWORDS.items():
        for kw in kwlist:
            if kw in text_n:
                return intent
    if "fee" in text_n:
        return "semester_fee"
    return "full_details"

def generate_answer(user_text: str) -> str:
    """Generate a chatbot response based on user input."""
    course = detect_course(user_text)
    intent = detect_intent(user_text)

    if not course:
        return (
            "Please specify a course. Available options: " +
            ", ".join(data.keys())
        )

    course_info = data.get(course, {})

    if intent == "full_details":
        parts = [f"{k.replace('_',' ').title()}: {v}" for k, v in course_info.items()]
        return f"Fee details for {course}:\n" + "\n".join(parts)
    else:
        key = intent
        value = course_info.get(key)
        if value:
            return f"{key.replace('_',' ').title()} for {course} is {value}."
        else:
            return f"Sorry, information about {key.replace('_',' ')} is not available for {course}."

# Test in terminal (optional)
if __name__ == "__main__":
    while True:
        txt = input("You: ")
        if txt.strip().lower() in ["exit", "quit"]:
            break
        print("Bot:", generate_answer(txt))
