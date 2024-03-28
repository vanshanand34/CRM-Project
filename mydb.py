import mysql.connector


dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'Poms@2004',
    port = '3006',
)

cursorObject = dataBase.cursor()
cursorObject.execute("show databases;")
print("all done! ")
