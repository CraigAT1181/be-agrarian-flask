from flask import Flask, request, jsonify
from flask_restful import Api
from flask_cors import CORS, cross_origin
from db.connection import get_connection
from dotenv import load_dotenv
import json
import os
from endpoints.fetch_all_produce import fetch_all_produce
from endpoints.fetch_all_users import fetch_all_users
from endpoints.fetch_users_by_produce_name import fetch_users_by_produce_name
from endpoints.fetch_conversations_by_user_id import fetch_conversations_by_user_id
from endpoints.authenticate_user import authenticate_user
from endpoints.add_user import add_new_user

load_dotenv()

app = Flask(__name__)
api = Api(app)
CORS(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

connection = get_connection()

# GET all endpoints
@app.route('/', methods=['GET'])
@cross_origin()
def get_endpoints():
    file = open('./endpoints.json')
    data = json.load(file)
    return data

# Get all produce
@app.route('/produce', methods=['GET'])
@cross_origin()
def get_all_produce():
    result = fetch_all_produce(connection)
    return result

# GET all users
@app.route('/users', methods=['GET'])
@cross_origin()
def get_all_users():
    result = fetch_all_users(connection)
    return result

# GET users by produce name
@app.route('/users/<produce_list>', methods=['GET'])
@cross_origin()
def get_users_by_produce_name(produce_list):
    result = fetch_users_by_produce_name(connection, produce_list.split(','))
    return result

# GET conversations by user id
@app.route('/users/<user_id>/conversations', methods=['GET'])
@cross_origin()
def get_conversations_by_user_id(user_id):
    result = fetch_conversations_by_user_id(connection, user_id)
    print(result)
    return result

if __name__ == '__main__':
    app.run(debug=True)

# POST authenticate user
@app.route('/authenticate', methods=["POST"])
@cross_origin() 
def check_authentication():
    data = request.get_json()
    return authenticate_user(connection, data)

# POST register user
@app.route('/users', methods=['POST'])
@cross_origin()
def register_user():
    data = request.get_json()
    result = add_new_user(data, connection)
    return jsonify(result)