# 🗓️ Day Challenge Tracker

A beautiful habit tracker built with **Flask + SQLite**. Data is saved permanently in a local database file — no browser storage issues.

## Setup

**1. Install Python** (3.8 or newer) from https://python.org

**2. Install Flask:**
```
pip install flask
```

**3. Run the app:**
```
python app.py
```

**4. Open your browser at:**
```
http://127.0.0.1:5000
```

That's it! The database file (`challenge.db`) is created automatically in the same folder and persists all your data forever.

## Features
- 90 / 100 / 180 / 365 day challenges
- Click any day to add tasks and subtasks
- Mark days as done
- Goal, reward, start date, notes
- Progress bar
- All data saved in SQLite (survives restarts, refreshes, anything)

## Files
```
challenge_app/
├── app.py              ← Python / Flask backend
├── requirements.txt    ← Dependencies
├── challenge.db        ← SQLite database (auto-created)
└── templates/
    └── index.html      ← Frontend (HTML/CSS/JS)
```
