from flask import jsonify, url_for
from utils.send_email import send_email
from utils.check_email_registered import check_email_registered
from endpoints.add_verification import add_verification
import secrets
import logging
import psycopg2

def password_reset_request(data, connection):

    try:
        email = data.get("email")

        if not email:
            return jsonify({"message": "No email received."}), 400

        if not check_email_registered(email, connection):
            return jsonify({"message": "This e-mail is not actually registered yet."}), 404
        
        token = secrets.token_urlsafe(20)
        
        verification_type = 'password_reset'

        add_verification(email, token, verification_type, connection)

        reset_link = f'https://cookingpot.live/set-new-password?token={token}'

        subject = 'Password Reset Request'
        body = f'Click the following link to reset your password: {reset_link}'

        send_email(subject, email, body)

        return jsonify({"message": "Passsword reset email sent successfully."}), 200

    except psycopg2.Error as e:
        # Log the database error
        logging.error(f"Database error: {e}")
        return jsonify({"message": "Database error occurred."}), 500

    except Exception as e:
        # Log the unexpected error
        logging.error(f"An unexpected error occurred: {e}")
        return jsonify({"message": "Failed to process the password reset request."}), 500

