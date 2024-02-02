from flask import jsonify, url_for
from utils.send_email import send_email
from endpoints.add_verification import add_verification
import secrets

def password_reset_request(token, data, connection):

    email = data["email"]

    if not email:
        return jsonify({"message": "No email received."}), 400
    
    if not token:
        token = secrets.token_urlsafe(20)
    
    verification_type = 'password_reset'

    add_verification(email, token, verification_type, connection)

    reset_link = url_for('initiate_password_reset', token=token, _external=True)
    subject = 'Password Reset Request'
    body = f'Click the following link to reset your password: {reset_link}'

    send_email(subject, email, body)

    return jsonify({"message": "Passsword reset email sent successfully."}), 200

