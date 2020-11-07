from tkinter import *
import mysql.connector

conn = mysql.connector.connect(user='root', password='123456', host='127.0.0.1')
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
    query_adding_user = "INSERT INTO `project_schema`.`user1` (`email`) VALUES ('"+entered_email+"');"
    cursor.execute(query_adding_user)
    print("Data is saved")



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


