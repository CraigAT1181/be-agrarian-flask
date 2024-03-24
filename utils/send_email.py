from flask_mail import Message
import logging

def send_email(subject, recipient, body):
    try:
        from api import mail
        
        if not subject or not recipient or not body:
            raise ValueError("Subject, recipient, or body cannot be empty.")
        
        msg = Message(subject, recipients=[recipient])
        msg.body = body

        mail.send(msg)

        logging.info("Email sent successfully to %s", recipient)
        
        return True

    except Exception as e:
        logging.error("Failed to send email to %s: %s", recipient, e)
        return False