from flask_mail import Message

def send_email(subject, recipient, body):
    from api import mail
    msg = Message(subject, recipients=[recipient])
    msg.body = body
    mail.send(msg)
