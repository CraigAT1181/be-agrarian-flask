from flask import Flask
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


if __name__ == '__main__':
    app.run(debug=True)
