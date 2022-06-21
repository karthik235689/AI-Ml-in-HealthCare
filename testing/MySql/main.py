import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="TOOR@toor"
)

mycursor=db.cursor()
mycursor.execute("CREATE DATABASE testdatabase")

