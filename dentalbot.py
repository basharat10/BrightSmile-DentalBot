import os
import google.generativeai as genai
import panel as pn
from dotenv import load_dotenv
import csv

# Load Environment variables from .env
_ = load_dotenv()  # reads GEMINI_API_KEY from .env

# Configure GenAI client
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create the model and open a chat session
model = genai.GenerativeModel("gemini-1.5-flash")
chat_session = model.start_chat(history=[])

system_text = """
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
"""

# Send system prompt into the session once
chat_session.send_message(system_text)

def gemini_chat(messages):
    """
    messages: List of dicts [{'role': 'user'/'assistant'/'system', 'content': '...'}]
    Returns the assistant’s reply (string) from the open chat_session.
    """
    user_text = messages[-1]["content"]
    response = chat_session.send_message(user_text)
    return response.text

def save_appointment_to_csv(text, file="appointments.csv"):
    import re
    name = re.search(r"(?:Name|name)[:\\-]?\\s*(\\w+)", text)
    service = re.search(r"(?:Service|service)[:\\-]?\\s*(\\w+)", text)
    date = re.search(r"(?:Date|date)[:\\-]?\\s*([\\w\\s]+)", text)
    time = re.search(r"(?:Time|time)[:\\-]?\\s*([\\w\\s:]+)", text)
    notes = re.search(r"(?:Notes|notes)[:\\-]?\\s*(.*)", text)

    row = [
        name.group(1) if name else "",
        service.group(1) if service else "",
        date.group(1) if date else "",
        time.group(1) if time else "",
        notes.group(1) if notes else ""
    ]

    with open(file, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(row)

# Conversation logic and Panel UI
messages = [
    {
        "role": "system",
        "content": """
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
    }
]

panels = []

def collect_messages(_):
    prompt = inp.value.strip()
    if not prompt:
        return pn.Column(*panels)

    messages.append({"role": "user", "content": prompt})
    inp.value = ""

    reply = gemini_chat(messages)
    messages.append({"role": "assistant", "content": reply})

    if "appointment" in reply.lower() and "confirmed" in reply.lower():
        save_appointment_to_csv(reply)

    panels.append(pn.Row("You:", pn.pane.Markdown(prompt, width=600)))
    panels.append(
        pn.Row(
            "DentalBot:",
            pn.pane.HTML(f"<div style='background-color:#F6F6F6; padding:8px'>{reply}</div>", width=600)
        )
    )

    return pn.Column(*panels)

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
