from tkinter import *

root = Tk()
root.title("Keywords input form")
root.geometry('800x300')

def close():
    root.destroy()
    root.quit()

frame_for_tip1=Frame(root, width=800, height=1,bd=10)
frame_for_email_field=Frame(root, width=800, height=2,bd=10)
frame_for_tip2=Frame(root, width=800, height=1,bd=10)
frame_for_keywords_field=Frame(root, width=800, height=2,bd=10)
frame_for_submit_button=Frame(root,bd=10, height=2, width=2)
tip1=Label(frame_for_tip1,text="Enter your email here:")
email_field = Text(frame_for_email_field, height=2, width=90)
tip2=Label(frame_for_tip2,text="Enter keywords here:")
keywords_field = Text(frame_for_keywords_field, height=2, width=90)
submit_button = Button(frame_for_submit_button, text="Submit")


frame_for_tip1.pack()
frame_for_email_field.pack()
frame_for_tip2.pack()
frame_for_keywords_field.pack()
frame_for_submit_button.pack()
tip1.pack()
keywords_field.pack()
tip2.pack()
email_field.pack()
submit_button.pack()

root.protocol('WM_DELETE_WINDOW', close)
root.mainloop()