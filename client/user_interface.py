from tkinter import *
import mysql.connector

conn = mysql.connector.connect(user='root', password='1234', host='169.254.19.167', database='project_schema')
cursor = conn.cursor()

root = Tk()
root.title("Keywords input form")
root.geometry('800x150')

def close():
    root.destroy()
    root.quit()

def button_clicked():
    entered_email=email_field.get()
    entered_keywords = keywords_field.get()
    print (entered_email)
    print (entered_keywords)
    query_adding_user = "INSERT INTO `user` (`email`) VALUES ('"+entered_email+"');"
    cursor.execute(query_adding_user)
    query_id = "SELECT id FROM project_schema.user WHERE email = '" + entered_email + "'"
    cursor.execute(query_id)
    id = cursor.fetchone()[0]
    id=str(id)
    query_adding_keywords = "INSERT INTO `user_keyword` (`user_id`,`keyword`) VALUES ('" +id+ "','"+entered_keywords+"');"
    cursor.execute(query_adding_keywords)
    conn.commit()

tip1=Label(root,text="Enter your email here:")
email_field = Entry(root, width=80)
tip2=Label(root,text="Enter keywords here:")
keywords_field = Entry(root, width=130)
submit_button = Button(root, text="Submit", width=15, height=3, activebackground="green", command=button_clicked)

tip1.pack()
email_field.pack()
tip2.pack()
keywords_field.pack()
submit_button.pack(side=BOTTOM)

root.mainloop()
conn.close()


