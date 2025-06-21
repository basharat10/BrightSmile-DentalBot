import os
import csv
import re
import panel as pn
from dotenv import load_dotenv
import google.generativeai as genai

# ---- Configuration ----

# Load environment variables from .env file (expects GEMINI_API_KEY)
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure GenAI client
genai.configure(api_key=GEMINI_API_KEY)
MODEL_NAME = "gemini-1.5-flash"

# System prompt for DentalBot
SYSTEM_PROMPT = """
You are DentalBot, a friendly assistant for BrightSmile Dental Clinic.
Your tasks:
  1. Greet the customer politely.
  2. If the user wants to book an appointment, ask step by step:
     - Their name
     - Service they need (cleaning, filling, check-up, etc.)
     - Preferred date and time
     - Any special notes (insurance, allergies, etc.)
     - Summarize their booking and confirm.
  3. If the user has a query (hours, insurance, policies), answer clearly.
  4. Always ask: 'Is there anything else I can help you with?'
  5. Respond in a short, conversational, friendly style.
""".strip()

# ---- GenAI Chat Session ----

def start_dentalbot_chat():
    """Start a chat session with the system prompt."""
    model = genai.GenerativeModel(MODEL_NAME)
    chat = model.start_chat(history=[])
    chat.send_message(SYSTEM_PROMPT)
    return chat

chat_session = start_dentalbot_chat()

def gemini_chat(messages):
    """
    Send the last user message in messages to the Gemini chat session.
    Args:
        messages: List of dicts [{'role': ..., 'content': ...}]
    Returns:
        Assistant's reply as string.
    """
    user_text = messages[-1]["content"]
    response = chat_session.send_message(user_text)
    return response.text

# ---- Appointment CSV Handling ----

def parse_appointment_details(text):
    """
    Extract appointment details from text using regex.
    Returns a dict with possible keys: name, service, date, time, notes.
    """
    patterns = {
        "name": r"(?:Name|name)\s*[:\-]?\s*([A-Za-z\s]+)",
        "service": r"(?:Service|service)\s*[:\-]?\s*([A-Za-z\s]+)",
        "date": r"(?:Date|date)\s*[:\-]?\s*([A-Za-z0-9,\-/ ]+)",
        "time": r"(?:Time|time)\s*[:\-]?\s*([A-Za-z0-9: ]+)",
        "notes": r"(?:Notes|notes)\s*[:\-]?\s*(.*)"
    }
    details = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        details[key] = match.group(1).strip() if match else ""
    return details

def save_appointment_to_csv(text, file="appointments.csv"):
    """
    Save appointment details extracted from text to a CSV file.
    """
    details = parse_appointment_details(text)
    row = [details["name"], details["service"], details["date"], details["time"], details["notes"]]
    header = ["Name", "Service", "Date", "Time", "Notes"]
    file_exists = os.path.isfile(file)
    with open(file, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)
        writer.writerow(row)

# ---- Conversation State and UI ----

messages = [{"role": "system", "content": SYSTEM_PROMPT}]
panels = []

def collect_messages(_):
    """
    Handle user input, update chat history, panel display, and save appointments if confirmed.
    """
    prompt = inp.value.strip()
    if not prompt:
        return pn.Column(*panels)

    # Add user message
    messages.append({"role": "user", "content": prompt})
    inp.value = ""

    # Get assistant reply
    reply = gemini_chat(messages)
    messages.append({"role": "assistant", "content": reply})

    # Save appointment if detected
    if "appointment" in reply.lower() and "confirmed" in reply.lower():
        save_appointment_to_csv(reply)

    # Update UI panels
    panels.append(pn.Row("You:", pn.pane.Markdown(prompt, width=600)))
    panels.append(
        pn.Row(
            "DentalBot:",
            pn.pane.HTML(
                f"<div style='background-color:#F6F6F6; padding:8px'>{reply}</div>",
                width=600
            )
        )
    )
    return pn.Column(*panels)

# ---- Panel UI Components ----

pn.extension()
inp = pn.widgets.TextInput(value="", placeholder="Type your message here…")
button = pn.widgets.Button(name="Send", button_type="primary")
interactive_conversation = pn.bind(collect_messages, button)

dashboard = pn.Column(
    "# BrightSmile DentalBot\n",
    pn.Row(inp, button),
    pn.panel(interactive_conversation, loading_indicator=True, height=300)
)

if __name__ == "__main__":
    pn.serve(dashboard, title="BrightSmile DentalBot")
