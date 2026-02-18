import sqlite3

# Connect to SQLite (in memory for testing)
conn = sqlite3.connect(':memory:')

# Turn ON foreign keys (important in SQLite)
conn.execute("PRAGMA foreign_keys = ON;")

cursor = conn.cursor()

# Helper function to inspect table contents
def print_table(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    print(f"\nTable: {table_name}")
    print(" | ".join(columns))
    print("-" * 40)

    for row in rows:
        print(" | ".join(str(value) for value in row))


# 1 Student table
cursor.execute("""
CREATE TABLE student (
    student_id INT PRIMARY KEY,
    name TEXT NOT NULL,
    age INT
)
""")

# 2️Registered courses table
cursor.execute("""
CREATE TABLE registered_courses (
    student_id INT,
    course_id INT,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id)
)
""")

# 3️Grades table
cursor.execute("""
CREATE TABLE grades (
    student_id INT,
    course_id INT,
    grade REAL,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES student(student_id)
)
""")

students = [
    (1, 'Alice', 20),
    (2, 'Bob', 22),
    (3, 'Charlie', 21)
]

registered = [
    (1, 101),
    (1, 102),
    (2, 101),
    (3, 103)
]

grades_data = [
    (1, 101, 85),
    (1, 102, 92),
    (2, 101, 78),
    (3, 103, 88)
]

cursor.executemany("INSERT INTO student VALUES (?, ?, ?)", students)
cursor.executemany("INSERT INTO registered_courses VALUES (?, ?)", registered)
cursor.executemany("INSERT INTO grades VALUES (?, ?, ?)", grades_data)

conn.commit()


print_table(cursor, "student")
print_table(cursor, "registered_courses")
print_table(cursor, "grades")


#MAXIMUM GRADE WITH COURSE AND STUDENT ID

cursor.execute("""
SELECT student_id, course_id, MAX(grade)
FROM grades
""")

print("\nMaximum grade with student and course:")
for row in cursor.fetchall():
    print(row)


# AVERAGE GRADE OF A STUDENT (example: student_id = 1)

cursor.execute("""
SELECT student_id, AVG(grade)
FROM grades
WHERE student_id = 1
""")

print("\nAverage grade for student 1:")
for row in cursor.fetchall():
    print(row)


conn.close()
