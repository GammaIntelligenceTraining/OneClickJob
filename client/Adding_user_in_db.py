import mysql.connector

conn = mysql.connector.connect(user='root', password='123456', host='127.0.0.1', database='project_schema')
cursor = conn.cursor()

query_adding_user="INSERT INTO `candidate` (`email`) VALUES ('something@some.com')"
cursor.execute(query_adding_user)

print("Log record inserted")

conn.close()
