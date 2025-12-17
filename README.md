# student_performance_tracker
This is a simple web-based Student Tracker application built using Flask and SQLite. It allows you to manage students, store their grades, view student details, and calculate average marks easily through a browser.

Features

Add new students with roll number and name

Add subject-wise grades for students

View student details along with all grades

Calculate average grade of a student

User-friendly interface with basic styling

Data stored locally using SQLite database

Tech Used

Python

Flask

SQLite

HTML

CSS

Project Structure
├── app.py
├── students.db
├── requirements.txt
├── Procfile
├── templates
│   ├── index.html
│   └── student.html
└── static
    └── style.css

How to Run the Project

Clone the repository

git clone https://github.com/your-username/student-tracker.git


Go to the project folder

cd student-tracker


Install required packages

pip install -r requirements.txt


Run the application

python app.py


Open your browser and visit

http://127.0.0.1:5000/

Usage

Use Add Student form to register a student

Use Add Grade to insert subject marks

Use View Student to see student details

Use Calculate Average to get average marks

Notes

Grades should be between 0 and 100

Roll number must be unique

Database is created automatically on first run
