# 🎓 University Examination Portal (Python + MySQL)

A **Command Line Interface (CLI)** based project for managing university examination records.  
It allows administrators to manage students, exams, and results while students can view their marks and grades.  
The system supports **MySQL database integration** as well as a **dictionary-based mode** for offline use.

---

## 🚀 Features

### 🧑‍💼 Admin Features
- Add, view, update, and delete student records  
- Add and manage exams  
- Enter and view exam results  
- Load bulk student data using Faker and Pandas  
- Dictionary-based CRUD operations (offline mode)

### 🎓 Student Features
- View personal exam results and overall grades  
- Get performance summary with calculated average and grade

---

## 🧠 Technologies Used
- **Python 3**
- **MySQL** (for data storage)
- **Pandas** (for data handling)
- **Faker** (for generating fake names)
- **CLI Menu System**

---

## 🗂️ Database Structure

### 1. `students` Table
| Field | Type | Description |
|--------|------|-------------|
| student_id | INT | Primary key |
| name | VARCHAR(100) | Student name |
| department | VARCHAR(100) | Student department |

### 2. `exams` Table
| Field | Type | Description |
|--------|------|-------------|
| exam_id | INT | Primary key |
| exam_name | VARCHAR(100) | Exam title |
| subject | VARCHAR(100) | Subject name |

### 3. `results` Table
| Field | Type | Description |
|--------|------|-------------|
| result_id | INT | Primary key |
| student_id | INT | Foreign key |
| exam_id | INT | Foreign key |
| marks | FLOAT | Marks scored |

---

## ⚙️ How to Run

1. **Install dependencies**
   ```bash
   pip install mysql-connector-python pandas faker

2. Create the MySQL Database

CREATE DATABASE university_portal;
USE university_portal;

3. Run the Script

python university_portal.py

4. Login Options

1. Admin Login (username: admin, password: admin123)
2. Student Login
3. Exit