from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Helper function to connect to the database
def get_db_connection():
    conn = sqlite3.connect('employee.db')
    conn.row_factory = sqlite3.Row  # This makes rows behave like dictionaries
    return conn

# Home page route that shows the login/logout form and attendance records
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all attendance records
    cursor.execute('SELECT * FROM attendance')
    attendance_records = cursor.fetchall()  # Get all records

    conn.close()
    
    return render_template('index.html', records=attendance_records)  # Pass records to the template

# Route to handle login
@app.route('/login', methods=['POST'])
def login():
    employee_id = request.form['employee_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Convert to string

    # Insert the login time into the attendance table
    cursor.execute('INSERT INTO attendance (employee_id, login_time) VALUES (?, ?)', (employee_id, login_time))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

# Route to handle logout
@app.route('/logout', methods=['POST'])
def logout():
    employee_id = request.form['employee_id']

    conn = get_db_connection()
    cursor = conn.cursor()
    logout_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Convert to string

    # Update the last record where logout_time is NULL (still logged in)
    cursor.execute('UPDATE attendance SET logout_time = ? WHERE employee_id = ? AND logout_time IS NULL',
                   (logout_time, employee_id))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
