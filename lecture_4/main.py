import random
import sqlite3

# Data for record generation
name=["helen", "mary", "aurora", "mike", "harry", "katie", "vera", "alice", "james", "vanya"]
last_name=["potter", "biven", "smith", "malfoy", "terra", "dogger", "niser", "diser", "pluss"]
subjects=["english", "russian", "math", "logic", "philosophy", "history", "informatics"]

# Generate student
def create_student():
    full_name = f"{random.choice(name)} {random.choice(last_name)}"
    birth_year = random.randint(2000, 2010)
    return full_name, birth_year

# Generate mark for random student
def create_mark(max_id=10):
    subject=random.choice(subjects)
    grade=random.randint(1, 10)
    id = random.randint(1, max_id)
    return id, subject, grade

# Main logic & work with database
def main():
    with sqlite3.connect('school.db') as connection:

        cursor= connection.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        # Students table creation
        cursor.execute("CREATE TABLE IF NOT EXISTS students ("
                       "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "full_name TEXT NOT NULL,"
                       "birth_year INTEGER NOT NULL)")

        # Grades table creation
        cursor.execute("CREATE TABLE IF NOT EXISTS grades ("
                       "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "student_id INTEGER NOT NULL,"
                       "subject TEXT NOT NULL,"
                       "grade INTEGER NOT NULL,"
                       "FOREIGN KEY (student_id) REFERENCES students(id)"
                       ");")

        # Complete tables
        for i in range (0, 10):
            student = create_student()
            cursor.execute("INSERT INTO students("
                           "full_name, birth_year)"
                           "VALUES (?, ?)", student)
        max_id=cursor.execute("SELECT MAX(id) FROM students").fetchone()[0]
        for i in range(0, 10):
            mark = create_mark(max_id)
            cursor.execute("INSERT INTO grades("
                           "student_id, subject, grade)"
                           "VALUES (?, ?, ?)", mark)

        # Select born after 2004 and print
        cursor.execute("SELECT full_name FROM students WHERE birth_year > 2004")
        table_students=cursor.fetchall()
        print("Born after 2004:")
        for student in table_students:
            print(student[0])

        # Get average for concrete student
        student_name=input("Enter student full name: ")
        cursor.execute("SELECT students.full_name,"
                       "ROUND(AVG(grades.grade),2) as avg_grade "
                       "FROM students "
                       "LEFT JOIN grades ON students.id=grades.student_id "
                       "WHERE LOWER(students.full_name) = ? "
                       "GROUP BY students.id ", (student_name,))
        result = cursor.fetchone()
        print(f"{result[0]} - {result[1]}")

        # Get average for every student
        cursor.execute("SELECT students.full_name, ROUND(AVG(grades.grade), 2) "
                       "FROM students "
                       "LEFT JOIN grades ON students.id=grades.student_id "
                       "GROUP BY students.id")
        for result in cursor.fetchall():
            print(f"{result[0]} - {result[1]}")

        # Get average grade for each subject
        cursor.execute("SELECT subject, ROUND(AVG(grades.grade), 2) "
                       "FROM grades "
                       "GROUP BY subject")
        for result in cursor.fetchall():
            print(f"{result[0]} - {result[1]}")

        # Get a list of students with grade < 8 in any subject
        cursor.execute("SELECT students.full_name "
                       "FROM students "
                       "INNER JOIN grades ON students.id=grades.student_id "
                       "WHERE grades.grade < 8 "
                       "GROUP BY students.id")
        for result in cursor.fetchall():
            print(result[0])

        # Get top 3 students
        cursor.execute("SELECT students.full_name,"
                       "ROUND(AVG(grades.grade),2) as avg_grade "
                       "FROM students "
                       "INNER JOIN grades ON students.id=grades.student_id "
                       "GROUP BY students.id "
                       "ORDER BY avg_grade DESC "
                       "LIMIT 3")
        for result in cursor.fetchall():
            print(f"{result[0]} - {result[1]}")

main()