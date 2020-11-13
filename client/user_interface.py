from tkinter import *
import mysql.connector
import re

conn = mysql.connector.connect(user='root', password='123456', host='127.0.0.1', database='project_schema')
cursor = conn.cursor()

def start_interface():
    root = Tk()
    root.title("Keywords input form")
    root.geometry('800x150')

    # function for the "Submit" button (saving email and keywords into DB and deleting data from fields)
    def button_clicked():

        # function sends query to the DB to insert email into the "user" table
        def query_adding_user():
            query_adding_user = "INSERT INTO `user` (`email`) VALUES ('" + entered_email + "');"
            cursor.execute(query_adding_user)

        # function gets user id from the DB, the "user" table
        def query_getting_id():
            query_getting_id = "SELECT id FROM project_schema.user WHERE email = '" + entered_email + "'"
            cursor.execute(query_getting_id)
            id = cursor.fetchone()[0]
            return id

        # function sends query to the DB to insert user id and keywords into the "user_keyword" table
        def query_adding_keywords():
            keyword_set = creation_keyword_set()
            for keyword in keyword_set:
                id = str(query_getting_id())
                query_adding_keywords = "INSERT INTO `user_keyword` (`user_id`,`keyword`) VALUES ('" + id + "','" + keyword + "');"
                cursor.execute(query_adding_keywords)
                conn.commit()

        # function creates keywords set from entered string (with deleting extra spaces and duplicate words)
        def creation_keyword_set():
            raw_keywords_list = entered_keywords.split(",")
            print(raw_keywords_list)
            keyword_list = []
            for raw_keyword in raw_keywords_list:
                keyword = raw_keyword.strip()
                keyword_list.append(keyword)
            print(keyword_list)
            keyword_set = set(keyword_list)
            print(keyword_set)
            return keyword_set

        # getting entered data from email and keywords fields
        entered_email = email_field.get()
        entered_keywords = keywords_field.get()
        print(entered_email)
        print(entered_keywords)
        # checking that the email is not in the DB and sending queries to the DB to add new user and keywords
        query_existance = "SELECT email FROM project_schema.user WHERE email = '" + entered_email + "'"
        cursor.execute(query_existance)
        exists = cursor.fetchall()
        if not exists:
            # fields validation
            regexp_email = re.compile("[\w]+@([\w-]+\.)+[\w-]+")
            regexp_keywords = re.compile("[\w]")
            if regexp_email.match(entered_email) and regexp_keywords.match(entered_keywords):
                query_adding_user()
                query_getting_id()
                creation_keyword_set()
                query_adding_keywords()
                tip3.configure(text="Data is saved", fg="green")  # display the "data is saved" message
            else:
                tip3.configure(text="Enter valid data",
                               fg="red")  # display text if the fields are empty or contains invalid data
        else:
            tip3.configure(text="Email is already exist", fg="red")  # display the "Email is already exist" message
        conn.commit()
        # delete data from email and keywords fields
        email_field.delete(0, END)
        keywords_field.delete(0, END)

    # create vidgets in the app window
    tip1 = Label(root, text="Enter your email here:")
    email_field = Entry(root, width=80)
    tip2 = Label(root, text="Enter keywords here:")
    keywords_field = Entry(root, width=130)
    tip3 = Label(root)
    submit_button = Button(root, text="Submit", width=15, height=3, activebackground="green", command=button_clicked)
    tip1.pack()
    email_field.pack()
    tip2.pack()
    keywords_field.pack()
    tip3.pack()
    submit_button.pack(side=BOTTOM)

    root.mainloop()
    conn.close()


start_interface()