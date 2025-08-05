from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_FILE = 'expenses.db'

# Create table if not exists
def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            date TEXT NOT NULL,
                            category TEXT NOT NULL,
                            description TEXT,
                            amount REAL NOT NULL
                          )''')
        conn.commit()
        conn.close()

@app.route('/', methods=['GET', 'POST'])
def home():
    message = None
    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        description = request.form['description']
        amount = request.form['amount']

        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?)',
                       (date, category, description, amount))
        conn.commit()
        conn.close()

        return redirect(url_for('home', message='Expense added successfully!'))

    message = request.args.get('message')
    return render_template('index.html', message=message)

@app.route('/view')
def view_expenses():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expenses ORDER BY date DESC')
    expenses = cursor.fetchall()
    conn.close()
    return render_template('view.html', expenses=expenses)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
