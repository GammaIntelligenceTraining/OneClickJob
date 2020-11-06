# password dsf342asda
# python@mrartful.com
# smtp: smtp.zone.eu port 465 SSL/TLS or 587 STARTTLS

import smtplib
from email.message import EmailMessage
import mysql.connector


# email_input = input('Please enter yout email: ')
email_input = 'roman.kutselepa@gmail.com'

# Connection to database

# conn = mysql.connector.connect(database='project_schema', host='localhost', user='root', password='123456789')
# cursor = conn.cursor()
# cursor.execute("SELECT usr.id, usr.email, email.title, email.message_body FROM project_schema.user_data AS usr "
#                "INNER JOIN project_schema.email AS email ON email.user_id = usr.id AND usr.email='" + email_input + "'")
# data = cursor.fetchone()
# user_id = data[0]
# email = data[1]
# email_title = data[2]
# email_body = data[3]
# print(data)

# Add data to MySQL table
# cursor.execute("INSERT INTO `user_data` (`email`) VALUES ('" + email_input + "')")

# cursor.execute("SELECT a.email, b.")


# Command to get user email and data to send from USER_DATA and EMAIL tables

'''SELECT usr.id, usr.email, email.title, email.message_body FROM project_schema.user_data AS usr
INNER JOIN project_schema.email AS email ON email.user_id = usr.id'''

# Creating email
msg = EmailMessage()
msg['Subject'] = 'Test message'
msg['From'] = 'python@mrartful.com'
msg['To'] = 'mr.artfulx@gmail.com'

msg.set_content('This is string sent by Python script')
msg.add_alternative("""\
        <!DOCTYPE html>
        <html>
            <body>
                <h1 style="color: red;">What is in a lava lamp and how does it work?</h1>
                <p style="color: grey;">This is a test message sent to you by a small script on Python</p>
                <p style="color: grey;">The lamp contains blobs of coloured wax inside a glass vessel filled with clear or translucent liquid; the wax rises and falls as its density changes due to heating from an incandescent light bulb underneath the vessel. The appearance of the wax is suggestive of pāhoehoe lava, hence the name.</p>
            </body>
        </html>
        """,
                    subtype='html')


# Sending email using smtp connection

with smtplib.SMTP_SSL('smtp.zone.eu', 465) as smtp:

    smtp.login('python@mrartful.com', 'dsf342asda')
    smtp.send_message(msg)