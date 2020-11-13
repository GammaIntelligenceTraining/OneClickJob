import mysql.connector

user = int(input("Enter user id"))

conn = mysql.connector.connect(user='root', password='1234', host='169.254.19.167', database='project_schema')
cursor = conn.cursor()

query_get_keywords = "SELECT keyword FROM project_schema.user_keyword where user_id=" + str(user)
print(query_get_keywords)
cursor.execute(query_get_keywords)
keywords_list = cursor.fetchall()
print(keywords_list)

for keyword in keywords_list:
    get_links_guery="select '" + str(user) + "', url from project_schema.crawler_1_data where plain_position_description " \
                    "LIKE '%"+str(keyword[0])+"%' or details LIKE '%" + str(keyword[0]) + "%';"
    insert_query = "INSERT INTO `project_schema`.`user_valid_links` (`user_id`,`link`) " \
                   + get_links_guery
    cursor.execute(insert_query)
    conn.commit()



