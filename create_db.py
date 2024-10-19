import sqlite3  # This is the library for working with SQLite databases

# Create or connect to a database called employee.db
conn = sqlite3.connect('employee.db')
cursor = conn.cursor()  # This allows us to execute SQL commands

# Create employees table to store employee details
cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    department TEXT NOT NULL)''')

# Create attendance table to track employee login and logout times
cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id INTEGER,
                    login_time DATETIME,
                    logout_time DATETIME,
                    FOREIGN KEY (employee_id) REFERENCES employees (id))''')

conn.commit()  # Save the changes to the database
conn.close()  # Close the database connection
