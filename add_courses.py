import sqlite3

conn = sqlite3.connect("student.db")
cursor = conn.cursor()

# Create tables if they don't exist yet
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT UNIQUE,
        department TEXT,
        password TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        course_id INTEGER PRIMARY KEY AUTOINCREMENT,
        course_name TEXT,
        instructor TEXT,
        credits INTEGER
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS enrollments (
        enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        course_id INTEGER
    )
""")

# Add password column to existing students if needed
try:
    cursor.execute("ALTER TABLE students ADD COLUMN password TEXT")
except Exception:
    pass

conn.commit()

courses = [
    ("Data Structures", "Dr Mehta", 4),
    ("Algorithms", "Dr Sharma", 4),
    ("Artificial Intelligence", "Dr Rao", 3),
    ("Machine Learning", "Dr Gupta", 3),
    ("Deep Learning", "Dr Singh", 3),
    ("Cyber Security", "Dr Khan", 3),
    ("Cloud Computing", "Dr Reddy", 3),
    ("Computer Networks", "Dr Patel", 3),
    ("Operating Systems", "Dr Das", 4),
    ("Software Engineering", "Dr Thomas", 3),
    ("Big Data Analytics", "Dr Iyer", 3),
    ("Blockchain Technology", "Dr Kapoor", 3),
]

cursor.executemany(
    "INSERT INTO courses(course_name, instructor, credits) VALUES(?, ?, ?)",
    courses
)

conn.commit()
conn.close()

print("Courses added successfully!")