import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Nhan2107@",  # đổi lại nếu cần
    database="emr_system"
)

cursor = conn.cursor(dictionary=True)

doctor_id = "d36ef9a4-7f3e-4458-bc71-2dc2390efb0f"

sql = "SELECT * FROM emr_visits WHERE doctor_id = %s"
params = (doctor_id,)

print("DEBUG SQL:", sql)
print("DEBUG PARAMS:", params)

cursor.execute(sql, params)
rows = cursor.fetchall()

print("KẾT QUẢ:", rows)

cursor.close()
conn.close()
