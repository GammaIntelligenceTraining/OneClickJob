from tkinter import *
import mysql.connector
import time

conn = mysql.connector.connect(user='root', password='123456', host='127.0.0.1', database='project_schema')
cursor = conn.cursor()

def start_interface():
    root = Tk()
    root.title("Keywords input form")
    root.geometry('800x150')

    #функция для кнопки "Submit", которая отправляет данные пользователя в БД
    #(эл почту, ключевые слова), а затем стрирает введенные данные из полей ввода
    def button_clicked():

        entered_email=email_field.get()
        entered_keywords = keywords_field.get()
        print (entered_email)
        print (entered_keywords)
        #проверка на пустой ввод
        if entered_email.isalnum() and entered_keywords.isalnum():
        #запись в БД эл почты юзера в таблицу "user"
            query_adding_user = "INSERT INTO `user` (`email`) VALUES ('"+entered_email+"');"
            cursor.execute(query_adding_user)

            #получение id записанного юзера из балицы "user"
            query_id = "SELECT id FROM project_schema.user WHERE email = '" + entered_email + "'"
            cursor.execute(query_id)
            id = cursor.fetchone()[0]
            id=str(id)

            #разбивка строки, которую ввел юзер на отдельные слова (кейворды) с удалением
            #лишних пробелов и одинаковых слов
            raw_keywords_list = entered_keywords.split(",")
            print(raw_keywords_list)
            keyword_list = []
            for raw_keyword in raw_keywords_list:
                keyword = raw_keyword.strip()
                keyword_list.append(keyword)
            print(keyword_list)
            keyword_set = set(keyword_list)
            print(keyword_set)

            #запись id юзера и кейвордов юзера в БД в таблицу "user_keyword"
            for keyword in keyword_set:
                query_adding_keywords = "INSERT INTO `user_keyword` (`user_id`,`keyword`) VALUES ('" +id+ "','"+keyword+"');"
                cursor.execute(query_adding_keywords)
                conn.commit()

            #вывод подсказки "данные сохранены"
            tip3.configure(text="Data is saved", fg="green")

        #вывод подскази "заполните все поля"
        else:
            tip3.configure(text="Fill in all the fields", fg="red")

        # удаление введенных данных в поля для ввода эл почты и ключевых слов
        email_field.delete(0, END)
        keywords_field.delete(0, END)

    #создание виджетов (текст подсказок, поле для ввода эл почты, поле для ввода ключевых слов,
    #кнопка "submit") в окне приложения
    tip1=Label(root,text="Enter your email here:")
    email_field = Entry(root, width=80)
    tip2=Label(root,text="Enter keywords here:")
    keywords_field = Entry(root, width=130)
    tip3=Label(root)
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
