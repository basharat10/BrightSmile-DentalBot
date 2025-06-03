# BrightSmile DentalBot

A simple, interactive Dental Clinic chatbot built with Google Gemini (gemini-1.5-flash) and Panel. Users can book dental appointments and ask common clinic questions—all through a friendly chat interface.

---

## 🚀 Features

- **Appointment Booking**  
  - Guides user step by step:  
    1. Collects patient name  
    2. Asks for service needed (e.g., cleaning, filling, check-up)  
    3. Asks for preferred date and time  
    4. Captures any additional notes (insurance, allergies, etc.)  
    5. Summarizes and confirms the booking  
  - Saves confirmed appointments to a local CSV file (`appointments.csv`)  

- **FAQ Handling**  
  - Answers common questions about:  
    - Clinic hours  
    - Accepted insurance  
    - Cancellation policy  
    - Location and contact info  

- **Interactive UI**  
  - Built with [Panel](https://panel.holoviz.org/)  
  - Displays user and bot messages in a scrollable chat panel  
  - Includes a DatePicker and TimePicker (for future enhancements)  

- **Easy to Extend**  
  - Modular code—add new features (e.g., email reminders) with minimal changes  
  - Clear separation between AI logic (`gemini_chat`) and UI (`collect_messages`)  

---

## 📋 Installation

1. **Clone this repository**  
   ```bash
   git clone https://github.com/basharat10/BrightSmile-DentalBot.git
   cd BrightSmile-DentalBot

   Create a Conda environment (requires Anaconda or Miniconda)

bash
Copy
Edit
conda create -n dentalbot_env python=3.9 -y
conda activate dentalbot_env
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Key packages:

google-generativeai (Gemini SDK)

panel (UI widgets)

python-dotenv (load API key securely)

Set up your API key

Create a file named .env in the project root.

Add your Gemini API key (replace YOUR_KEY):

ini
Copy
Edit
GEMINI_API_KEY=YOUR_KEY
▶️ Usage
Run the chatbot script

bash
Copy
Edit
python dental_bot.py
Panel will spin up a local server (default: http://localhost:5006).

Open your browser at that address to interact.

Chat with DentalBot

Type greetings or “I want to book an appointment.”

Follow the prompts—provide your name, service, date/time, and any notes.

Once “confirmed,” the appointment gets appended to appointments.csv.

Ask FAQs like “What are your hours?” or “Do you accept insurance B?”

View saved appointments

Open appointments.csv in Excel, LibreOffice, or any text editor.

Each line contains:

pgsql
Copy
Edit
Name,Service,Date,Time,Notes
🛠️ Project Structure
bash
Copy
Edit
BrightSmile-DentalBot/
├── dental_bot.py         # Main chatbot script
├── requirements.txt      # List of needed Python packages
├── .gitignore            # Excludes .env and other unneeded files
└── README.md             # This file
dental_bot.py

Imports and configures Gemini SDK

Defines gemini_chat() to send messages and receive replies

Defines save_appointment_to_csv() to record confirmed bookings

Defines collect_messages() for Panel UI logic

Starts Panel server when run as a script

appointments.csv (created at runtime)

Stores each confirmed appointment as a new row

🤝 Contributing
Contributions are welcome! You might consider:

Adding more FAQ shortcuts (e.g., “What’s your address?” returns a canned response).

Integrating email or SMS reminders using services like Twilio or SMTP.

Switching to a database (SQLite, PostgreSQL) for storing appointments.

Improving date/time picking: show pickers only when requested by the bot.

Feel free to submit a pull request or open an issue if you find bugs or have feature ideas.

📖 References
Google Generative AI Python SDK

Panel Documentation

python-dotenv on PyPI

📫 Contact
Basharat Ullah

GitHub: @basharat10

Email: basharatdotani.bd@gmail.com

Feel free to reach out if you have questions or suggestions!
