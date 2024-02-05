def check_email_registered(email, connection):
    query = """
    SELECT email FROM users WHERE email = %s;
    """

    with connection:
        cursor = connection.cursor()
        cursor.execute(query, (email,))
        is_registered = cursor.fetchone()

        return bool(is_registered)
