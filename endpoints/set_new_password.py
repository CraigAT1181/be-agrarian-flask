from flask import request

def set_new_password(data, connection):

    token = data['token']
    new_password = data['new_password']

    print(token, "<<<<TOKEN!")
    print(new_password, "<<<<<<NEW PASSWORD!")
    