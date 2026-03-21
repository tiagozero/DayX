from flask import Flask, render_template, request, jsonify
import sqlite3, json, os

app = Flask(__name__)
DB = os.path.join(os.path.dirname(__file__), 'challenge.db')

# ── DB SETUP ──────────────────────────────────────────────────────────────────
def get_db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with get_db() as con:
        con.executescript("""
            CREATE TABLE IF NOT EXISTS settings (
                key   TEXT PRIMARY KEY,
                value TEXT
            );
            CREATE TABLE IF NOT EXISTS days (
                day_number  INTEGER PRIMARY KEY,
                done        INTEGER DEFAULT 0
            );
            CREATE TABLE IF NOT EXISTS tasks (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                day_number  INTEGER NOT NULL,
                text        TEXT    NOT NULL,
                checked     INTEGER DEFAULT 0,
                position    INTEGER DEFAULT 0,
                FOREIGN KEY (day_number) REFERENCES days(day_number)
            );
            CREATE TABLE IF NOT EXISTS subtasks (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id     INTEGER NOT NULL,
                text        TEXT    NOT NULL,
                checked     INTEGER DEFAULT 0,
                position    INTEGER DEFAULT 0,
                FOREIGN KEY (task_id) REFERENCES tasks(id)
            );
        """)

init_db()

# ── HELPERS ───────────────────────────────────────────────────────────────────
def get_setting(key, default=None):
    with get_db() as con:
        row = con.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
        return row['value'] if row else default

def set_setting(key, value):
    with get_db() as con:
        con.execute("INSERT OR REPLACE INTO settings(key,value) VALUES(?,?)", (key, str(value)))

def load_full_state():
    duration   = int(get_setting('duration', 100))
    goal       = get_setting('goal', '')
    reward     = get_setting('reward', '')
    start_date = get_setting('start_date', '')
    note       = get_setting('note', '')

    with get_db() as con:
        days_rows = con.execute("SELECT * FROM days").fetchall()
        tasks_rows = con.execute("SELECT * FROM tasks ORDER BY position").fetchall()
        subs_rows  = con.execute("SELECT * FROM subtasks ORDER BY position").fetchall()

    # Build subs lookup
    subs_by_task = {}
    for s in subs_rows:
        subs_by_task.setdefault(s['task_id'], []).append({
            'id': s['id'], 'text': s['text'],
            'checked': bool(s['checked'])
        })

    # Build tasks lookup
    tasks_by_day = {}
    for t in tasks_rows:
        tasks_by_day.setdefault(t['day_number'], []).append({
            'id': t['id'], 'text': t['text'],
            'checked': bool(t['checked']),
            'open': False,
            'subs': subs_by_task.get(t['id'], [])
        })

    # Build days dict
    days = {}
    for d in days_rows:
        n = d['day_number']
        days[n] = {
            'done': bool(d['done']),
            'tasks': tasks_by_day.get(n, [])
        }
    # Fill in days that only have tasks but no days row
    for n, tlist in tasks_by_day.items():
        if n not in days:
            days[n] = {'done': False, 'tasks': tlist}

    return {
        'duration': duration, 'goal': goal, 'reward': reward,
        'startDate': start_date, 'note': note, 'days': days
    }

# ── ROUTES ────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/state', methods=['GET'])
def api_get_state():
    return jsonify(load_full_state())

@app.route('/api/settings', methods=['POST'])
def api_settings():
    data = request.json
    for key in ('duration', 'goal', 'reward', 'startDate', 'note'):
        if key in data:
            db_key = 'start_date' if key == 'startDate' else key
            set_setting(db_key, data[key])
    return jsonify({'ok': True})

@app.route('/api/day/<int:n>/done', methods=['POST'])
def api_day_done(n):
    done = 1 if request.json.get('done') else 0
    with get_db() as con:
        con.execute("INSERT OR REPLACE INTO days(day_number,done) VALUES(?,?)", (n, done))
    return jsonify({'ok': True})

@app.route('/api/day/<int:n>/tasks', methods=['GET'])
def api_get_tasks(n):
    with get_db() as con:
        tasks = con.execute("SELECT * FROM tasks WHERE day_number=? ORDER BY position", (n,)).fetchall()
        subs  = con.execute(
            "SELECT s.* FROM subtasks s JOIN tasks t ON s.task_id=t.id WHERE t.day_number=? ORDER BY s.position", (n,)
        ).fetchall()
    subs_by_task = {}
    for s in subs:
        subs_by_task.setdefault(s['task_id'], []).append({
            'id': s['id'], 'text': s['text'], 'checked': bool(s['checked'])
        })
    result = []
    for t in tasks:
        result.append({
            'id': t['id'], 'text': t['text'], 'checked': bool(t['checked']),
            'open': False, 'subs': subs_by_task.get(t['id'], [])
        })
    return jsonify(result)

@app.route('/api/task', methods=['POST'])
def api_add_task():
    data = request.json
    with get_db() as con:
        con.execute("INSERT OR IGNORE INTO days(day_number,done) VALUES(?,0)", (data['day'],))
        cur = con.execute(
            "INSERT INTO tasks(day_number,text,checked,position) VALUES(?,?,0,"
            "(SELECT COALESCE(MAX(position)+1,0) FROM tasks WHERE day_number=?))",
            (data['day'], data['text'], data['day'])
        )
        task_id = cur.lastrowid
    return jsonify({'id': task_id})

@app.route('/api/task/<int:tid>', methods=['PATCH'])
def api_edit_task(tid):
    data = request.json
    with get_db() as con:
        if 'text' in data:
            con.execute("UPDATE tasks SET text=? WHERE id=?", (data['text'], tid))
        if 'checked' in data:
            con.execute("UPDATE tasks SET checked=? WHERE id=?", (1 if data['checked'] else 0, tid))
    return jsonify({'ok': True})

@app.route('/api/task/<int:tid>', methods=['DELETE'])
def api_delete_task(tid):
    with get_db() as con:
        con.execute("DELETE FROM subtasks WHERE task_id=?", (tid,))
        con.execute("DELETE FROM tasks WHERE id=?", (tid,))
    return jsonify({'ok': True})

@app.route('/api/task/<int:tid>/subtask', methods=['POST'])
def api_add_subtask(tid):
    data = request.json
    with get_db() as con:
        cur = con.execute(
            "INSERT INTO subtasks(task_id,text,checked,position) VALUES(?,?,0,"
            "(SELECT COALESCE(MAX(position)+1,0) FROM subtasks WHERE task_id=?))",
            (tid, data['text'], tid)
        )
        sub_id = cur.lastrowid
    return jsonify({'id': sub_id})

@app.route('/api/subtask/<int:sid>', methods=['PATCH'])
def api_edit_subtask(sid):
    data = request.json
    with get_db() as con:
        if 'text' in data:
            con.execute("UPDATE subtasks SET text=? WHERE id=?", (data['text'], sid))
        if 'checked' in data:
            con.execute("UPDATE subtasks SET checked=? WHERE id=?", (1 if data['checked'] else 0, sid))
    return jsonify({'ok': True})

@app.route('/api/subtask/<int:sid>', methods=['DELETE'])
def api_delete_subtask(sid):
    with get_db() as con:
        con.execute("DELETE FROM subtasks WHERE id=?", (sid,))
    return jsonify({'ok': True})

@app.route('/api/reset', methods=['POST'])
def api_reset():
    with get_db() as con:
        con.executescript("""
            DELETE FROM subtasks;
            DELETE FROM tasks;
            DELETE FROM days;
            DELETE FROM settings;
        """)
    return jsonify({'ok': True})

if __name__ == '__main__':
    print("\n🚀  Challenge Tracker running at http://127.0.0.1:5000\n")
    app.run(debug=True)
