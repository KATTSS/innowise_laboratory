import sqlite3
with sqlite3.connect('school.db') as connection:

    cursor= connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS students ("
                   "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "full_name TEXT NOT NULL,"
                   "birth_year INTEGER NOT NULL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS grades ("
                   "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                   "student_id INTEGER NOT NULL,"
                   "subject TEXT NOT NULL,"
                   "grade INTEGER NOT NULL,"
                   "FOREIGN KEY (student_id) REFERENCES students(id)"
                   ");")


