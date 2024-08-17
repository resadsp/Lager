import sqlite3
connection = sqlite3.connect("./orders.db")
cursor = connection.cursor()



cursor.execute("INSERT INTO avgust VALUES (?,?);",("01.08.2024", 850))             
#cursor.execute("DELETE FROM avgust;")             
connection.commit()

cursor.close()
connection.close()