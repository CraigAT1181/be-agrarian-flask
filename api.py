from flask import Flask
from flask_restful import Api
from flask_cors import CORS, cross_origin
from db.connection import get_connection
from dotenv import load_dotenv
import json
import os
from endpoints.fetch_users_by_produce_name import fetch_users_by_produce_name
from endpoints.fetch_all_produce import fetch_all_produce

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

# GET users by produce_id
@app.route('/users/<produce_name>', methods=['GET'])
@cross_origin()
def get_users_by_produce_name(produce_name):
    result = fetch_users_by_produce_name(connection, produce_name)
    return result

if __name__ == '__main__':
    app.run(debug=True)
