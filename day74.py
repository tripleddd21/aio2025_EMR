import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nhan2107@",
    database="test")

cursor = conn.cursor()
print("Connected to database")

# Create a new database

cursor.execute(""" 
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    age INT NOT NULL
)
""")
print("Table created successfully")

# Insert a new record
students=[("Nguyen Duc Nhan", "n@gmail.com", 20),
          ("Nguyen Duc B", "b@gmail.com", 250),
          ("Nguyen van C", "c@gmail.com", 26)]
sql = "INSERT INTO students (name, email, age) VALUES (%s, %s, %s)"
for student in students:
    val = student
    cursor.execute(sql, val)
conn.commit()
print("Record inserted successfully")

# Qurey the database students in 18-22 years old
print("List of students in 18-22 years old")
sql1 = "SELECT * FROM students WHERE age BETWEEN 18 AND 22"
cursor.execute(sql1)
for row in cursor.fetchall():
    print(row)

# Update a record
print("Update record")
sql2 = "UPDATE students SET email = 'BBB@gmail.com' WHERE name = 'Nguyen Duc B'"
cursor.execute(sql2)
conn.commit()
print("Record updated successfully")

# Find studends has name "Nhan"
print("List of students has name 'Nhan'")
sql3 = "SELECT * FROM students WHERE name LIKE '%Nhan%'"
cursor.execute(sql3)
for row in cursor.fetchall():
    print(row)

# Group by age
print("List of students group by age")
sql4 = "SELECT age, COUNT(*) as total FROM students GROUP BY age ORDER BY age"
cursor.execute(sql4)
for row in cursor.fetchall():
    print("Age: ", row[0], "Total: ", row[1])
cursor.close()
conn.close()
print("Connection closed")



