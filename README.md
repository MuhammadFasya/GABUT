# 🎮 GABUT - Gamer Budget Tracker

**GABUT** (Gamer Budget Tracker) is a simple desktop financial management application built with Python and Tkinter. It is designed for gamers to easily track their income and expenses in an intuitive graphical interface.

---

## 🧩 Features

- Add, edit, and delete transactions
- Categorize income and expenses
- Dashboard with financial charts
- Dark mode support
- Responsive window (supports maximize/minimize)
- "Back" button for easy navigation
- Local data storage using JSON

---

## 📁 Project Structure

GABUT/
├── data/ # Folder for storing transaction data
├── models/ # Core logic and model classes
│ ├── init.py
│ ├── expense.py
│ ├── expense_tracker.py
│ ├── finance_manager.py
│ ├── transaction.py
├── venv/ # Python virtual environment (optional)
├── main.py # Main GUI application entry point
├── README.md # Project documentation
├── requirements.txt # Project dependencies
└── tempCodeRunnerFile.py # Temporary script for quick testing

---

## 🚀 Getting Started

### 1. Clone this repository

```bash
git clone https://github.com/yourusername/gabut.git
cd gabut
```

### 2. Create and activate a virtual environment

python -m venv venv

# On Windows:

venv\Scripts\activate

# On macOS/Linux:

source venv/bin/activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Run the Application

python main.py

📦 Dependencies
All dependencies are listed in requirements.txt. The app uses:

tkinter for GUI

matplotlib or similar (if chart/graph is used)

🤝 Contributing
Feel free to fork the project and submit a pull request. Suggestions, improvements, and new features are welcome!

📜 License
This project is licensed under the MIT License.
