from flask import Flask, render_template, request, redirect, flash
import sqlite3
from pathlib import Path
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for flash messages

# Get the directory containing this script
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'students.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS students (
        roll_number TEXT PRIMARY KEY,
        name TEXT NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS grades (
        roll_number TEXT,
        subject TEXT,
        grade INTEGER,
        FOREIGN KEY (roll_number) REFERENCES students (roll_number)
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_student', methods=['POST'])
def add_student():
    try:
        name = request.form['name'].strip()
        roll = request.form['roll'].strip()
        
        if not name or not roll:
            flash('Name and Roll Number are required')
            return redirect('/')
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO students VALUES (?, ?)", (roll, name))
        conn.commit()
        flash(f'Student {name} added successfully!')
        
    except sqlite3.Error as e:
        flash(f'Error adding student: {str(e)}')
    except Exception as e:
        flash(f'An error occurred: {str(e)}')
    finally:
        conn.close()
    return redirect('/')

@app.route('/add_grade', methods=['POST'])
def add_grade():
    try:
        roll = request.form['roll'].strip()
        subject = request.form['subject'].strip()
        
        if not roll or not subject:
            flash('Roll number and subject are required')
            return redirect('/')
            
        try:
            grade = int(request.form['grade'])
            if not (0 <= grade <= 100):
                flash('Grade must be between 0 and 100')
                return redirect('/')
        except ValueError:
            flash('Grade must be a valid number')
            return redirect('/')
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Check if student exists
        c.execute("SELECT name FROM students WHERE roll_number=?", (roll,))
        if not c.fetchone():
            flash(f'Student with roll number {roll} does not exist!')
            return redirect('/')
            
        c.execute("INSERT INTO grades VALUES (?, ?, ?)", (roll, subject, grade))
        conn.commit()
        flash('Grade added successfully!')
        
    except sqlite3.Error as e:
        flash(f'Error adding grade: {str(e)}')
    except Exception as e:
        flash(f'An error occurred: {str(e)}')
    finally:
        conn.close()
    return redirect('/')

@app.route('/view_student', methods=['GET'])
def view_student():
    try:
        roll = request.args.get('roll', '').strip()
        if not roll:
            flash('Roll number is required')
            return redirect('/')
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT name FROM students WHERE roll_number=?", (roll,))
        student = c.fetchone()
        
        if not student:
            flash('Student not found')
            return redirect('/')
        
        c.execute("SELECT subject, grade FROM grades WHERE roll_number=?", (roll,))
        grades = c.fetchall()
        return render_template('student.html', student=student, grades=grades, roll=roll)
    
    except sqlite3.Error as e:
        flash(f'Error retrieving student data: {str(e)}')
        return redirect('/')
    finally:
        conn.close()

@app.route('/average', methods=['GET'])
def average():
    try:
        roll = request.args.get('roll', '').strip()
        if not roll:
            return 'Roll number is required'
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # Check if student exists
        c.execute("SELECT name FROM students WHERE roll_number=?", (roll,))
        if not c.fetchone():
            return f'Student with roll number {roll} not found'
        
        c.execute("SELECT grade FROM grades WHERE roll_number=?", (roll,))
        grades = [row[0] for row in c.fetchall()]
        
        if not grades:
            return f'No grades recorded for {roll}'
        
        avg = sum(grades) / len(grades)
        return f"Average Grade for {roll}: {avg:.2f}"
    
    except sqlite3.Error as e:
        return f'Error calculating average: {str(e)}'
    except Exception as e:
        return f'An error occurred: {str(e)}'
    finally:
        conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
