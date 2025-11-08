from faker import Faker
import mysql.connector
import pandas as pd

# ------------------ DATABASE CONNECTION ------------------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="03032008",  
        database="university_portal"1

    )

# Initialize Faker
fake = Faker()
Faker.seed(3)

# ------------------ LOAD DATA FROM CSV ------------------
def load_data():
    conn = connect_db()
    cursor = conn.cursor()
     
    cursor.execute("SELECT COUNT(*) FROM students")
    existing_count = cursor.fetchone()[0]

    if existing_count > 0:
        print(f"Database already has {existing_count} records. Skipping data load to prevent duplication.")
        conn.close()
        return
    
    df = pd.read_csv("StudentsPerformance.csv")
    df['name'] = [fake.name() for _ in range(len(df))]

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO students 
            (name, gender, parental_education, lunch, test_preparation_course, math_score, reading_score, writing_score)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            row['name'], 
            row['gender'],
            row['parental level of education'],
            row['lunch'],
            row['test preparation course'],
            row['math score'],
            row['reading score'],
            row['writing score']
        ))

    conn.commit()
    conn.close()
    print("Data loaded successfully into MySQL")

# ------------------ ADMIN FUNCTIONS (SQL) ------------------
def add_student():
    conn = connect_db()
    cursor = conn.cursor()
    name = input("Enter name: ")
    gender = input("Enter gender: ")
    parental_education = input("Enter parental education: ")
    lunch = input("Enter lunch type: ")
    test_preparation = input("Enter test preparation course: ")
    math = int(input("Enter math score: "))
    reading = int(input("Enter reading score: "))
    writing = int(input("Enter writing score: "))

    cursor.execute("""
        INSERT INTO students (name, gender, parental_education, lunch, test_preparation_course, math_score, reading_score, writing_score)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (name, gender, parental_education, lunch, test_preparation, math, reading, writing))

    conn.commit()
    conn.close()
    print("Student added successfully!")

def view_students():
    conn = connect_db()
    df = pd.read_sql("SELECT * FROM students", conn)
    df.set_index("id", inplace=True)
    print(df)
    conn.close()

def update_student():
    conn = connect_db()
    cursor = conn.cursor()
    student_id = int(input("Enter Student ID to update: "))

    print("\nWhat do you want to update?")
    print("1. Math Score")
    print("2. Reading Score")
    print("3. Writing Score")
    print("4. All Scores")
    choice = input("Enter choice: ")

    if choice == "1":
        new_math = int(input("Enter new math score: "))
        cursor.execute("UPDATE students SET math_score=%s WHERE id=%s", (new_math, student_id))
    elif choice == "2":
        new_reading = int(input("Enter new reading score: "))
        cursor.execute("UPDATE students SET reading_score=%s WHERE id=%s", (new_reading, student_id))
    elif choice == "3":
        new_writing = int(input("Enter new writing score: "))
        cursor.execute("UPDATE students SET writing_score=%s WHERE id=%s", (new_writing, student_id))
    elif choice == "4":
        new_math = int(input("Enter new math score: "))
        new_reading = int(input("Enter new reading score: "))
        new_writing = int(input("Enter new writing score: "))
        cursor.execute("""
            UPDATE students 
            SET math_score=%s, reading_score=%s, writing_score=%s
            WHERE id=%s
        """, (new_math, new_reading, new_writing, student_id))
    else:
        print("Invalid choice.")
        conn.close()
        return

    conn.commit()
    conn.close()
    print("Student record updated successfully!")

def delete_student():
    conn = connect_db()
    cursor = conn.cursor()
    student_id = int(input("Enter Student ID to delete: "))
    cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
    conn.commit()
    conn.close()
    print("Student deleted successfully!")

# ------------------ CLIENT FUNCTION (SQL) ------------------
def view_result():
    conn = connect_db()
    student_id = int(input("Enter your Student ID: "))
    df = pd.read_sql(f"SELECT * FROM students WHERE id={student_id}", conn)
    if df.empty:
        print("Student not found.")
    else:
        print("\n=== STUDENT RESULT ===")
        print(df)
        avg = (df['math_score'].iloc[0] + df['reading_score'].iloc[0] + df['writing_score'].iloc[0]) / 3
        print(f"\nAverage Score: {avg:.2f}")
        if avg >= 90:
            print("Grade: S")
        elif avg >= 80:
            print("Grade: A")
        elif avg >= 70:
            print("Grade: B")
        elif avg >= 60:
            print("Grade: C")
        else:
            print("Grade: D")
    conn.close()

# ------------------ DICTIONARY BASED STUDENT DATA ------------------
students_dict = [
    {"id": 1, "name": "Aarav Sharma", "gender": "Male", "parental_education": "Bachelor’s", "lunch": "standard", "test_preparation_course": "none", "math_score": 85, "reading_score": 78, "writing_score": 80},
    {"id": 2, "name": "Diya Patel", "gender": "Female", "parental_education": "Master’s", "lunch": "free/reduced", "test_preparation_course": "completed", "math_score": 92, "reading_score": 89, "writing_score": 95},
    {"id": 3, "name": "Rohan Singh", "gender": "Male", "parental_education": "Highschool", "lunch": "standard", "test_preparation_course": "none", "math_score": 68, "reading_score": 74, "writing_score": 70},
    {"id": 4, "name": "Ananya Gupta", "gender": "Female", "parental_education": "Bachelor’s", "lunch": "standard", "test_preparation_course": "completed", "math_score": 88, "reading_score": 92, "writing_score": 90},
    {"id": 5, "name": "Krish Mehta", "gender": "Male", "parental_education": "Some college", "lunch": "standard", "test_preparation_course": "none", "math_score": 60, "reading_score": 65, "writing_score": 70},
    {"id": 6, "name": "Ishita Reddy", "gender": "Female", "parental_education": "Highschool", "lunch": "free/reduced", "test_preparation_course": "none", "math_score": 75, "reading_score": 72, "writing_score": 74},
    {"id": 7, "name": "Vikram Nair", "gender": "Male", "parental_education": "Master’s", "lunch": "standard", "test_preparation_course": "completed", "math_score": 95, "reading_score": 98, "writing_score": 94},
    {"id": 8, "name": "Meera Iyer", "gender": "Female", "parental_education": "Some college", "lunch": "standard", "test_preparation_course": "none", "math_score": 78, "reading_score": 82, "writing_score": 80},
    {"id": 9, "name": "Arjun Rao", "gender": "Male", "parental_education": "Bachelor’s", "lunch": "standard", "test_preparation_course": "completed", "math_score": 84, "reading_score": 88, "writing_score": 86},
    {"id": 10, "name": "Neha Das", "gender": "Female", "parental_education": "Master’s", "lunch": "free/reduced", "test_preparation_course": "none", "math_score": 70, "reading_score": 75, "writing_score": 72}
]


# ------------------ DICTIONARY CRUD FUNCTIONS ------------------

# View all dictionary data
def show_dict_data():
    df = pd.DataFrame(students_dict)
    df.set_index("id", inplace=True)
    print(df)


# Add new student to dictionary
def add_dict_student():
    new_id = len(students_dict) + 1
    name = input("Enter name: ")
    gender = input("Enter gender: ")
    parental_education = input("Enter parental education: ")
    lunch = input("Enter lunch type: ")
    test_preparation = input("Enter test preparation course: ")
    math = int(input("Enter math score: "))
    reading = int(input("Enter reading score: "))
    writing = int(input("Enter writing score: "))

    students_dict.append({
        "id": new_id,
        "name": name,
        "gender": gender,
        "parental_education": parental_education,
        "lunch": lunch,
        "test_preparation_course": test_preparation,
        "math_score": math,
        "reading_score": reading,
        "writing_score": writing
    })
    print("Student added successfully to dictionary!")

# Update existing student record in dictionary
def update_dict_student():
    sid = int(input("Enter Student ID to update: "))
    for student in students_dict:
        if student["id"] == sid:
            print("\n1. Math Score\n2. Reading Score\n3. Writing Score\n4. All Scores")
            choice = input("Enter choice: ")
            if choice == "1":
                student["math_score"] = int(input("Enter new math score: "))
            elif choice == "2":
                student["reading_score"] = int(input("Enter new reading score: "))
            elif choice == "3":
                student["writing_score"] = int(input("Enter new writing score: "))
            elif choice == "4":
                student["math_score"] = int(input("Enter new math score: "))
                student["reading_score"] = int(input("Enter new reading score: "))
                student["writing_score"] = int(input("Enter new writing score: "))
            print("Student record updated successfully in dictionary!")
            return
    print("Student ID not found in dictionary.")

# Delete a student from dictionary
def delete_dict_student():
    sid = int(input("Enter Student ID to delete: "))
    global students_dict
    students_dict = [s for s in students_dict if s["id"] != sid]
    print("Student deleted from dictionary.")

# ------------------ ADMIN MENU (SQL + DICTIONARY) ------------------
def admin_menu():
    while True:
        print("\n=== ADMIN MENU ===")
        print("1. Add Student")
        print("2. View Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Load Dataset")
        print("6. Logout")
        print("7. Use Dictionary Data (No SQL/CSV)")
        choice = input("Enter choice: ")

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            update_student()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            load_data()
        elif choice == "6":
            break
        elif choice == "7":
            while True:
                print("\n=== DICTIONARY DATA MENU ===")
                print("1. View All Students")
                print("2. Add Student")
                print("3. Update Student")
                print("4. Delete Student")
                print("5. Back to Admin Menu")
                sub_choice = input("Enter choice: ")

                if sub_choice == "1":
                    show_dict_data()
                elif sub_choice == "2":
                    add_dict_student()
                elif sub_choice == "3":
                    update_dict_student()
                elif sub_choice == "4":
                    delete_dict_student()
                elif sub_choice == "5":
                    break
                else:
                    print("Invalid choice.")

        else:
            print("Invalid choice.")

# ------------------ CLIENT MENU (SQL) ------------------
def client_menu():
    while True:
        print("\n=== CLIENT MENU ===")
        print("1. View My Result")
        print("2. Logout")
        choice = input("Enter choice: ")

        if choice == "1":
            view_result()
        elif choice == "2":
            break
        else:
            print("Invalid choice.")

# ------------------ MAIN MENU ------------------
def main():
    while True:
        print("\n=== UNIVERSITY EXAM PORTAL ===")
        print("1. Admin Login")
        print("2. Student Login")
        print("3. Exit")
        user = input("Enter your choice: ")

        if user == "1":
            username = input("Enter admin username: ")
            password = input("Enter admin password: ")
            if username == "admin" and password == "admin123":
                admin_menu()
            else:
                print("Invalid admin credentials.")
        elif user == "2":
            client_menu()
        elif user == "3":
            print("Exiting...")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
