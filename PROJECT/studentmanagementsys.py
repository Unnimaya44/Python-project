import sqlite3

conn = sqlite3.connect("student.db")
cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT)
    ''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        course TEXT,
        marks INTEGER,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id))
    ''')

conn.commit()


cursor.execute("SELECT * FROM users WHERE username=?", ("admin",))
data = cursor.fetchone()

if data:
    cursor.execute('''
        UPDATE users
        SET password=?, role=?
        WHERE username=?
    ''', ("1234", "admin", "admin"))
else:
    cursor.execute('''
        INSERT INTO users(username,password,role)
        VALUES(?,?,?)
    ''', ("admin", "1234", "admin"))

conn.commit()

print("Database and tables created successfully!")


def register():

    name = input("Enter username: ")
    password = input("Enter password: ")

    if name == "" or password == "":
        print("Fields cannot be empty!")
        return

    try:
        cursor.execute('''
            INSERT INTO users(username,password,role)
            VALUES(?,?,?)
        ''', (name, password, "staff"))

        conn.commit()
        print("Registration successful!")

    except sqlite3.IntegrityError:
        print("Username already exists!")


def login():

    print("\n--- LOGIN MENU ---")
    print("1. Admin Login")
    print("2. Staff Login")

    try:
        ch = int(input("Enter your choice: "))

        if ch == 1:
            role = "admin"
        elif ch == 2:
            role = "staff"

        else:
            print("Invalid choice!")
            return

        name = input("Enter username: ")
        password = input("Enter password: ")

        cursor.execute('''
            SELECT * FROM users
            WHERE username=? AND password=? AND role=?
        ''', (name, password, role))

        data = cursor.fetchone()

        if data:
            print("Login successful!")

            user_id = data[0]

            if role == "admin":
                adminmenu(user_id)

            else:
                staffmenu(user_id)

        else:
            print("Invalid username or password!")

    except ValueError:
        print("Enter a valid choice!")


def addstudent(user_id):

    name = input("Enter student name: ")
    course = input("Enter course: ")

    if name == "" or course == "":
        print("Fields cannot be empty!")
        return

    try:
        marks = int(input("Enter marks: "))

        if marks < 0 or marks > 100:
            print("Enter marks between 0 and 100!")

        else:
            cursor.execute('''
                INSERT INTO students(name,course,marks,user_id)
                VALUES(?,?,?,?)
            ''', (name, course, marks, user_id))

            conn.commit()
            print("Student added successfully!")

    except ValueError:
        print("Enter valid marks!")


def viewstudent():

    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()

    if data:
        print("\n--- STUDENT DETAILS ---")
        print("ID\tNAME\tCOURSE\tMARKS")

        for i in data:
            print(i[0], "\t", i[1], "\t", i[2], "\t", i[3])

    else:
        print("No students found!")


def updatestudent():

    try:
        s_id = int(input("Enter student ID to update: "))

        cursor.execute("SELECT * FROM students WHERE id=?", (s_id,))
        data = cursor.fetchone()

        if data:
            print("\nCurrent Student Details:")
            print("Name:", data[1])
            print("Course:", data[2])
            print("Marks:", data[3])

            print("\nEnter New Details:")

            name = input("Enter new name: ")
            course = input("Enter new course: ")
            marks = int(input("Enter new marks: "))

            if name.strip() == "" or course.strip() == "":
                print("Fields cannot be empty!")
                return

            if marks < 0 or marks > 100:
                print("Enter marks between 0 and 100!")
                return

            cursor.execute('''
                UPDATE students
                SET name=?, course=?, marks=?
                WHERE id=?
            ''', (name, course, marks, s_id))

            conn.commit()

            print("Student updated successfully!")

        else:
            print("Student ID not found!")

    except ValueError:
        print("Please enter valid details!")

    except sqlite3.Error as e:
        print("Database Error:", e)

def deletestudent():

    try:
        s_id = int(input("Enter student ID: "))

        cursor.execute("SELECT * FROM students WHERE id=?", (s_id,))
        data = cursor.fetchone()

        if data:
            ch = input("Are you sure you want to delete? y/n: ")

            if ch.lower() == "y":
                cursor.execute(
                    "DELETE FROM students WHERE id=?", (s_id,)
                )

                conn.commit()
                print("Student deleted successfully!")

            else:
                print("Cancelled!")

        else:
            print("Student not found!")

    except ValueError:
        print("Enter a valid ID!")


def adminmenu(user_id):

    while True:

        print("\n--- ADMIN MENU ---")

        try:
            ch = int(input(" 1. Add Student\n 2. View Student\n 3. Update Student\n 4. Delete Student\n 5. Logout\n Enter your choice:"))
        
        except ValueError:
            print("Please enter a valid number!")
            continue
        
        if ch == 1:
            addstudent(user_id)
        elif ch == 2:
            viewstudent()
        elif ch == 3:
            updatestudent()
        elif ch == 4:
            deletestudent()
        elif ch == 5:
            print("Logout successful!")
            break

        else:
            print("Invalid choice!")


def staffmenu(user_id):

    while True:

        print("\n--- STAFF MENU ---")
        try:
            ch = int(input("1. View Students\n 2. Logout\n Enter your choice: "))

        except ValueError:
                print("Please enter a valid number!")
                continue
        
        if ch == 1:
            viewstudent()
        elif ch == 2:
            print("Logout successful!")
            break

        else:
            print("Invalid choice!")


def main():

    print("\nWELCOME TO STUDENT MANAGEMENT SYSTEM")

    while True:
        
        try:
            ch = int(input("1. Register\n 2. Login\n 3. Exit\n Enter your choice: "))
        except ValueError:
                print("Please enter a valid number!")
                continue

        if ch == 1:
            register()
        elif ch == 2:
            login()
        elif ch == 3:
            print("Thank you!")
            break

        else:
            print("Invalid choice!")


main()

conn.close()