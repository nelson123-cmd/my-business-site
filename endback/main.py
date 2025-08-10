import os
import sqlite3
from flask import Flask, request, render_template, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# === Define Absolute Path to SQLite File ===
DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')

# === SETUP: Create SQLite DB and tables if not exist ===
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            date TEXT,
            time TEXT,
            special_request TEXT
        )
    ''')

    # Create messages table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            subject TEXT,
            message TEXT
        )
    ''')

    conn.commit()
    conn.close()

init_db()

# === HOME ROUTE ===
@app.route('/')
def home():
    return render_template('index.html')

# === CONTACT FORM HANDLING ===
@app.route('/contact', methods=['POST'])
def contact():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    # Save to SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO messages (name, email, subject, message)
        VALUES (?, ?, ?, ?)
    ''', (name, email, subject, message))
    conn.commit()
    conn.close()

    return '''
    <html>
        <body style="font-family: Arial; text-align: center; padding-top: 50px;">
        <h2>THANK YOU FOR CONTACTING US.</h2>
        <h3>We have received your message.</h3>
        <a href="https://my-business-site-eta.vercel.app/">
            <button>Back to Home</button>
        </a>
    </body>
    </html>
    '''

# === VIEW CONTACT MESSAGES ===
@app.route('/messages', methods=['GET'])
def show_messages():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, subject, message FROM messages")
    rows = cursor.fetchall()
    conn.close()

    html = "<h2>Contact Messages</h2><table border='1'><tr><th>Name</th><th>Email</th><th>Subject</th><th>Message</th></tr>"
    for row in rows:
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>"
    html += "</table>"
    return html

# === BOOKING FORM HANDLING ===
@app.route('/booking', methods=['POST'])
def handle_booking():
    name = request.form.get('name')
    email = request.form.get('email')
    date = request.form.get('date')
    time = request.form.get('time')
    special = request.form.get('special_request')

    # Save to SQLite
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO bookings (name, email, date, time, special_request)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, email, date, time, special))
    conn.commit()
    conn.close()

    return '''
    <html>
    <body style="font-family: Arial; text-align: center; padding-top: 50px;">
        <h2>THANK YOU FOR BOOKING YOUR TOUR WITH US.</h2>
        <h3>We will contact you via email.</h3>
        <a href="https://my-business-site-eta.vercel.app/">
            <button>Back to Homepage</button>
        </a>
    </body>
    </html>
    '''

# === VIEW BOOKINGS ===
@app.route('/bookings', methods=['GET'])
def show_bookings():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, date, time, special_request FROM bookings")
    rows = cursor.fetchall()
    conn.close()

    html = "<h2>Bookings</h2><table border='1'><tr><th>Name</th><th>Email</th><th>Date</th><th>Time</th><th>Special Request</th></tr>"
    for row in rows:
        html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>"
    html += "</table>"
    return html

# === PASSWORD-PROTECTED DOWNLOAD OF DB ===
@app.route('/download-db')
def download_db():
    password = request.args.get("password")
    if password != "vulnerabiliti":  # set your password here
        return "Unauthorized", 403
    return send_file('data.db', as_attachment=True)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)
