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
   git clone https://github.com/yourusername/BrightSmile-DentalBot.git
   cd BrightSmile-DentalBot
