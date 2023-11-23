from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS
from db.connection import get_connection
from dotenv import load_dotenv
import os

import json

load_dotenv()

app = Flask(__name__)
api = Api(app)
CORS(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

connection = get_connection()

# GET all endpoints
class Endpoints(Resource):
    def get(self):
        file = open("./endpoints.json")
        data = json.load(file)
        return data

api.add_resource(Endpoints, '/')

if __name__ == '__main__':
    app.run(debug=True)
