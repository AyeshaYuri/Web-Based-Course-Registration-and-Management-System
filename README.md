
# 🎓 Web-Based Course Registration and Management System

A **Flask-based web application** that allows students to register, log in, browse courses, and enroll in them. The system also provides an admin view to monitor students, courses, and enrollments.



## 📌 Features

### 👨‍🎓 Student Features

* User Registration & Login (Session-based authentication)
* View available courses
* Enroll in courses
* Prevent duplicate enrollments
* View enrolled courses after successful registration

### 🛠️ Admin Features

* View all registered students
* View all courses
* View student enrollments


## 🏗️ Tech Stack

* **Backend:** Python (Flask)
* **Frontend:** HTML, CSS (Jinja2 Templates)
* **Database:** SQLite3
* **Session Management:** Flask Sessions



## 📂 Project Structure

```
Course_enrollment/
│
├── app.py                  # Main Flask application
├── student.db              # SQLite database (auto-created)
│
├── templates/              # HTML templates
│   ├── home.html
│   ├── register.html
│   ├── login.html
│   ├── courses.html
│   ├── enrollment_success.html
│   ├── enrollments.html
│   └── admin.html
│
├── static/                 # CSS/JS files (optional)
│
├── requirements.txt
└── README.md
```



## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/AyeshaYuri/Web-Based-Course-Registration-and-Management-System
cd Web-Based-Course-Registration-and-Management-System
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install flask
```

### 4️⃣ Run the Application

```bash
python app.py
```



## 🚀 Usage

1. Open browser and go to:

```
http://127.0.0.1:5000/
```

2. Register a new student account
3. Login with credentials
4. Browse courses and enroll
5. View enrollment confirmation



## 🗄️ Database Schema

### 📌 Students Table

* `student_id` (Primary Key)
* `name`
* `email` (Unique)
* `department`
* `password`

### 📌 Courses Table

* `course_id` (Primary Key)
* `course_name`
* `instructor`
* `credits`

### 📌 Enrollments Table

* `enrollment_id` (Primary Key)
* `student_id` (Foreign Key)
* `course_id` (Foreign Key)


## 🔒 Security Notes

* Passwords are stored in **plain text** (⚠️ Not recommended for production)
* Suggested improvement:

  * Use `werkzeug.security` for password hashing
  * Implement role-based authentication for admin



## 🧠 Learning Outcomes

* Flask routing & request handling
* Session management
* SQLite database integration
* CRUD operations
* MVC architecture using templates



## 👩‍💻 Author

**Ayesha**
