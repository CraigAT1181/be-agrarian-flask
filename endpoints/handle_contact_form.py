from utils.send_email import send_email
from flask import jsonify, request

def handle_contact_form(data):
    try:
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        # Validate the form data
        if not name or not email or not message:
            return jsonify({"error": "Please provide name, email, and message"}), 400

        # Compose email subject and body
        subject = "New Contact Form Submission"
        body = f"Name: {name}\nEmail: {email}\nMessage: {message}"

        # Send email notification
        send_email(subject, "craig@cookingpot.live", body)

        return jsonify({"message": "Contact form submitted successfully"})
    except Exception as e:
        print("Error handling contact form:", e)
        return jsonify({"error": "Failed to submit contact form"}), 500