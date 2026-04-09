from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"


def get_db():
    conn = sqlite3.connect("student.db")
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

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
            course_id INTEGER,
            FOREIGN KEY(student_id) REFERENCES students(student_id),
            FOREIGN KEY(course_id) REFERENCES courses(course_id)
        )
    """)

    # Add password column to existing students table if it doesn't exist
    try:
        cursor.execute("ALTER TABLE students ADD COLUMN password TEXT")
    except Exception:
        pass

    conn.commit()
    conn.close()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    success = None

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        dept = request.form["dept"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO students(name, email, department, password) VALUES(?, ?, ?, ?)",
                (name, email, dept, password)
            )
            conn.commit()
            success = "Registration successful! You can now log in."
        except sqlite3.IntegrityError:
            error = "This email is already registered. Please log in."
        finally:
            conn.close()

    return render_template("register.html", error=error, success=success)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM students WHERE email=? AND password=?",
            (email, password)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            session["student_id"] = user["student_id"]
            session["student_name"] = user["name"]
            return redirect("/courses")
        else:
            error = "Invalid email or password. Please try again."

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/courses")
def courses():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    data = cursor.fetchall()
    conn.close()
    return render_template("courses.html", courses=data)


@app.route("/enroll", methods=["POST"])
def enroll():
    if "student_id" not in session:
        return redirect("/login")

    course_id = request.form["course_id"]
    student_id = session["student_id"]

    conn = get_db()
    cursor = conn.cursor()

    # Check if already enrolled
    cursor.execute(
        "SELECT * FROM enrollments WHERE student_id=? AND course_id=?",
        (student_id, course_id)
    )
    existing = cursor.fetchone()

    if existing:
        conn.close()
        return redirect("/enrollment_success?status=already_enrolled&course_id={}".format(course_id))

    cursor.execute(
        "INSERT INTO enrollments(student_id, course_id) VALUES(?, ?)",
        (student_id, course_id)
    )
    conn.commit()

    # Fetch the course details to show on success page
    cursor.execute("SELECT * FROM courses WHERE course_id=?", (course_id,))
    course = cursor.fetchone()
    conn.close()

    return redirect("/enrollment_success?status=success&course_id={}".format(course_id))


@app.route("/enrollment_success")
def enrollment_success():
    if "student_id" not in session:
        return redirect("/login")

    status = request.args.get("status", "success")
    course_id = request.args.get("course_id")
    student_id = session["student_id"]

    conn = get_db()
    cursor = conn.cursor()

    # Get the course details
    cursor.execute("SELECT * FROM courses WHERE course_id=?", (course_id,))
    course = cursor.fetchone()

    # Get all enrolled courses for this student
    cursor.execute("""
        SELECT courses.course_name, courses.instructor, courses.credits
        FROM enrollments
        JOIN courses ON enrollments.course_id = courses.course_id
        WHERE enrollments.student_id = ?
    """, (student_id,))
    enrolled = cursor.fetchall()
    conn.close()

    return render_template("enrollment_success.html",
                           course=course,
                           enrolled=enrolled,
                           status=status,
                           student_name=session.get("student_name", "Student"))


@app.route("/enrollments")
def enrollments():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT students.name, courses.course_name, courses.instructor, courses.credits
        FROM enrollments
        JOIN students ON enrollments.student_id = students.student_id
        JOIN courses ON enrollments.course_id = courses.course_id
        ORDER BY students.name
    """)
    data = cursor.fetchall()
    conn.close()
    return render_template("enrollments.html", data=data)


@app.route("/admin")
def admin():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    cursor.execute("""
        SELECT students.name, courses.course_name
        FROM enrollments
        JOIN students ON enrollments.student_id = students.student_id
        JOIN courses ON enrollments.course_id = courses.course_id
    """)
    enrollments = cursor.fetchall()
    conn.close()
    return render_template("admin.html", students=students, courses=courses, enrollments=enrollments)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)