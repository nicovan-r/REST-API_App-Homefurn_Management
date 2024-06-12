import mysql.connector

newdb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    )

my_cursor = newdb.cursor()

my_cursor.execute("CREATE DATABASE furniture_db")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)