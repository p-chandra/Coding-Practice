import smtplib
from email.mime.text import MIMEText

subject = "Email Subject"
body = "Text me when you get this"
sender = "sender@gmail.com"
recipients = ["someone@gmail.com", "test@gmail.com"]
password = ""


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Its a Me Mario'] = subject
    msg['Enter Name'] = sender
    msg['Koopa'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")


send_email(subject, body, sender, recipients, password)