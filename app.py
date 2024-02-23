from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize the SQLite database
conn = sqlite3.connect('tasks.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        date TEXT NOT NULL,
        complete INTEGER NOT NULL
    )
''')
conn.commit()
conn.close()

def get_tasks():
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tasks')
    tasks = [{'id': row[0], 'text': row[1], 'date': row[2], 'complete': row[3]} for row in c.fetchall()]
    conn.close()
    return tasks

def add_task(text, date):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('INSERT INTO tasks (text, date, complete) VALUES (?, ?, 0)', (text, date))
    conn.commit()
    conn.close()

def update_task(task_id, text, date):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('UPDATE tasks SET text=?, date=? WHERE id=?', (text, date, task_id))
    conn.commit()
    conn.close()

def complete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('UPDATE tasks SET complete=1 WHERE id=?', (task_id,))
    conn.commit()
    conn.close()

def incomplete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    c = conn.cursor()
    c.execute('UPDATE tasks SET complete=0 WHERE id=?', (task_id,))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    tasks = get_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task_route():
    task_text = request.form.get('task')
    task_date = request.form.get('date')
    add_task(task_text, task_date)
    return redirect(url_for('index'))

@app.route('/complete_task/<int:task_id>')
def complete_task_route(task_id):
    complete_task(task_id)
    return redirect(url_for('index'))

@app.route('/incomplete_task/<int:task_id>')
def incomplete_task_route(task_id):
    incomplete_task(task_id)
    return redirect(url_for('index'))

@app.route('/edit_task/<int:task_id>')
def edit_task(task_id):
    tasks = get_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    return render_template('edit.html', task=task)

@app.route('/update_task/<int:task_id>', methods=['POST'])
def update_task_route(task_id):
    task_text = request.form.get('task')
    task_date = request.form.get('date')
    update_task(task_id, task_text, task_date)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
