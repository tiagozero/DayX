# 📅 Day Challenge Tracker

A full-featured personal challenge tracker built with Flask + SQLite on the backend and a single-file HTML/JS/CSS frontend. Track multi-day challenges, recurring habits, daily tasks, and personal goals — all in one place.

---

## Features

### 🗓️ Challenge Grid
- Choose a challenge duration: **30, 60, 90, 100, 180, or 365 days**
- Set a **goal**, **reward**, and **start date**
- Each day is a clickable cell — open it to log tasks, notes, a rating, and challenger progress
- Cells show color-coded status: completed (green), rated (warm/cool tint), today (highlighted border), future (locked)
- A **▶ Start** button on Day 1 sets today as the start date instantly

### ⏱️ Clock & Countdown
- Live **clock** and **date** displayed at the top
- Shows the **current day number** and a **countdown to midnight** (turns red under 30 minutes)
- 🔥 **Streak counter** — consecutive completed days

### ✅ Tasks
- Add tasks to any day with a title, **priority level** (🔴 High / 🟡 Medium / 🟢 Low), and a **time estimate**
- Tasks support **subtasks** (nested checklist)
- **Roll-over control**: uncompleted tasks automatically carry forward to the next day; toggle 🚫↩ per task to opt out
- Rolled-over tasks show a "↩ Day N" badge so you know their origin

### 📋 Task Templates
- Save the current day's task set as a named template
- Apply any template to a day with one click
- Right-click a template chip to delete it

### 🎯 Challengers
- Create sub-challenges within your main challenge (e.g. *Read 10 books in 20 days*)
- Set a **total target**, **unit name**, **duration**, and **start day**
- Each challenger spans a range of days — those cells get an orange stripe at the top
- Use **+/−** buttons inside each day modal to log daily progress
- Add **steps** to any challenger (a checklist of milestones/tasks specific to that challenge)
- Choose from **8 built-in templates**: Read 12 Books, Run 100km, Meditate 30 Days, Write 50k Words, Workout 60x, Learn Guitar 100h, No Sugar 30 Days, Save $1000

### 🔁 Daily Habits
- Define recurring habits (e.g. *Drink 2L water*, *Meditate*, *Stretch*)
- They appear in every day's modal as a checklist
- Edit or delete habits from the **Edit** panel at any time
- Habit completions are stored per-day

### ⭐ Day Rating
- Rate each day 1–5 stars directly from the modal
- Unfinished days reflect their rating as a background tint on the grid cell

### 📊 Stats Dashboard
- **9 summary cards**: days complete, current streak, best streak, total tasks, tasks done, avg rating, challenger units, task time logged, completion rate
- **Bar chart**: completion rate by day of week
- **Rating distribution** chart

### 📅 Weekly Review
- Navigate week by week with ‹ › arrows
- 7-day grid showing completion status and star ratings
- Summary cards: days completed, tasks done, avg rating, completion rate

### 👤 Multi-Profile
- Create multiple independent challenge profiles (e.g. *Fitness Q1*, *Reading 2026*)
- Each profile has its own state, challengers, habits, and task templates
- Switch instantly from the dropdown in the top bar

### 💾 Import / Export
- **Export** dumps your full profile data (state, challengers, habits, templates) to a `.json` file
- **Import** restores from any previously exported file

### 🌙 Dark Mode
- Toggle between light and dark themes with the ☀️/🌙 button
- Preference is saved to `localStorage` and restored on every page load/refresh
- Light mode is the default

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python · Flask |
| Database | SQLite (via Flask) |
| Frontend | Vanilla HTML / CSS / JS (single file) |
| Fonts | Google Fonts — Playfair Display + DM Sans |
| Persistence (extra) | `localStorage` for profiles, challengers, habits, templates, theme |

---

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone or download the project
git clone https://github.com/your-username/day-challenge-tracker.git
cd day-challenge-tracker

# Install dependencies
pip install flask

# Run the server
python app.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

### First Steps

1. **Set your goal** in the Goal field (e.g. *Build a daily reading habit*)
2. **Set a reward** for completing the challenge
3. Click **▶ Start** on Day 1, or manually pick a start date
4. Click any day cell to open it and start logging tasks, habits, and notes
5. Add a **Challenger** (e.g. Read 10 books in 20 days) from the right panel
6. Mark the day as **✓ Done** when you've finished everything

---

## API Endpoints

The Flask backend exposes these endpoints used by the frontend:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/state` | Load full challenge state |
| `POST` | `/api/settings` | Save duration, goal, reward, start date |
| `GET` | `/api/day/:day/tasks` | Load tasks for a specific day |
| `POST` | `/api/day/:day/done` | Mark a day done / save note |
| `POST` | `/api/task` | Create a new task |
| `PATCH` | `/api/task/:id` | Update task text or checked state |
| `DELETE` | `/api/task/:id` | Delete a task |
| `POST` | `/api/task/:id/subtask` | Add a subtask |
| `PATCH` | `/api/subtask/:id` | Update subtask |
| `DELETE` | `/api/subtask/:id` | Delete subtask |
| `POST` | `/api/reset` | Reset all progress |

---

## Data Storage

- **SQLite** stores the core challenge state: days, tasks, subtasks, and settings
- **`localStorage`** stores profiles, challengers, habits, task templates, and the UI theme preference — this means they persist across browser sessions without needing the backend

---

## Project Structure

```
day-challenge-tracker/
├── app.py              # Flask application & SQLite logic
├── index.html          # Full frontend (single file)
├── README.md           # This file
└── challenge.db        # SQLite database (auto-created on first run)
```

---

## License

MIT — use it, fork it, build on it.
