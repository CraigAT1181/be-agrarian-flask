from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from db.config import load_jwt_config
from db.connection import get_connection
from dotenv import load_dotenv
import json
import os
from endpoints.fetch_all_produce import fetch_all_produce
from endpoints.fetch_all_users import fetch_all_users
from endpoints.fetch_users_by_produce_name import fetch_users_by_produce_name
from endpoints.fetch_conversations_by_user_id import fetch_conversations_by_user_id
from endpoints.fetch_messages_by_conversation_id import fetch_messages_by_conversation_id
from endpoints.authenticate_user import authenticate_user
from endpoints.password_reset_request import password_reset_request
from endpoints.set_new_password import set_new_password
from endpoints.add_new_user import add_new_user
from endpoints.remove_user_by_user_id import remove_user_by_user_id
from endpoints.patch_produce_by_user_id import patch_produce_by_user_id
from endpoints.fetch_all_posts import fetch_all_posts
from endpoints.add_post import add_new_post
from endpoints.remove_post_by_post_id import remove_post_by_post_id
from endpoints.add_message import add_message
from endpoints.add_conversation import add_conversation
from endpoints.remove_conversation_by_conversation_id import remove_conversation_by_conversation_id
from endpoints.handle_contact_form import handle_contact_form
from endpoints.fetch_all_ads import fetch_all_ads
from endpoints.fetch_all_blogs import fetch_all_blogs
from endpoints.fetch_comments_by_blog_id import fetch_comments_by_blog_id
from endpoints.fetch_blog_by_blog_id import fetch_blog_by_blog_id
from endpoints.fetch_blogs_by_user_id import fetch_blogs_by_user_id
from endpoints.add_blog import add_blog
from endpoints.remove_blog_by_blog_id import remove_blog_by_blog_id
from endpoints.patch_blog_by_blog_id import patch_blog_by_blog_id
from endpoints.add_comment import add_comment
from endpoints.patch_comment_by_comment_id import patch_comment_by_comment_id
from endpoints.remove_comment_by_comment_id import remove_comment_by_comment_id
from endpoints.shopify.fetch_products import fetch_products

if os.getenv('FLASK_ENV') == 'production':
    load_dotenv('.env.production')
else:
    load_dotenv('.env.development')

app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)
CORS(app)

jwt_config = load_jwt_config()
app.config['JWT_SECRET_KEY'] = jwt_config['SECRET_KEY']
jwt = JWTManager(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'craigtipple81@gmail.com'
app.config['MAIL_PASSWORD'] = 'fouj tuof cvsa oyln'
app.config['MAIL_DEFAULT_SENDER'] = 'craig@cookingpot.live'
mail = Mail(app)

connection = get_connection()

# Check which env Flask is running in
flask_env = os.getenv('FLASK_ENV')
print(f"FLASK_ENV value: {flask_env}")

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

# GET all ads
@app.route('/ads', methods=['GET'])
@cross_origin()
def get_all_ads():
    result = fetch_all_ads(connection)
    return result

# GET all users
@app.route('/users', methods=['GET'])
@cross_origin()
def get_all_users():
    result = fetch_all_users(connection)
    return result

# GET all blogs
@app.route('/blogs', methods=['GET'])
@cross_origin()
def get_all_blogs():
    result = fetch_all_blogs(connection)
    return result

# GET blog by blog id
@app.route('/blogs/<blog_id>', methods=['GET'])
@cross_origin()
def get_blog_by_blog_id(blog_id):
    result = fetch_blog_by_blog_id(blog_id, connection)
    return result

# GET blog by user id
@app.route('/users/<user_id>/blogs', methods=['GET'])
@cross_origin()
def get_blog_by_user_id(user_id):
    result = fetch_blogs_by_user_id(user_id, connection)
    return result

# POST blog
@app.route('/blogs', methods=["POST"])
@cross_origin()
def add_blog_by_user_id():
    try:

        if 'image' in request.files:
            image = request.files['image']
        else:
            image = None

        title = request.form.get('title')
        author_id = request.form.get('author_id')
        content = request.form.get('content')
        tags = request.form.getlist('tags')

        print("Received data:")
        print("Image:", image)
        print("Title:", title)
        print("Author ID:", author_id)
        print("Content:", content)
        print("Tags:", tags)

        return add_blog(image, title, author_id, content, tags, connection)
    except Exception as e:
        return {
            "message": str(e),
            "status": 400,
        }

# PATCH blog by blog_id
@app.route("/blogs/<blog_id>", methods=["PATCH"])
@cross_origin() 
def edit_blog_by_blog_id(blog_id):
    try:
        if 'image' in request.files:
            image = request.files['image']
        elif 'image' in request.form:
            image = request.form.get('image')
        elif 'image' not in request.files and 'image' not in request.form:
            image = None


        title = request.form.get('title')
        author_id = request.form.get('author_id')
        content = request.form.get('content')
        tags = request.form.getlist('tags')

        print("Received data:")
        print("Image:", image)
        print("Title:", title)
        print("Author ID:", author_id)
        print("Content:", content)
        print("Tags:", tags)
        print("Image Type:", type(image))
        print("Image Value:", image)

        return patch_blog_by_blog_id(blog_id, image, title, author_id, content, tags, connection)
    
    except Exception as e:
        return {
            "message": str(e),
            "status": 400,
        }

# DELETE blog by blog id
@app.route("/blogs/<blog_id>", methods=["DELETE"])
@cross_origin() 
def delete_blog_by_blog_id(blog_id):
    return remove_blog_by_blog_id(blog_id, connection)

# GET comments by blog id
@app.route("/blogs/<blog_id>/comments", methods=["GET"])
@cross_origin()
def get_comments_by_blog_id(blog_id):
    result = fetch_comments_by_blog_id(blog_id, connection)
    return result

# POST comment by blog id
@app.route('/blogs/<blog_id>/comments', methods=['POST'])
@cross_origin()
def add_comment_by_blog_id(blog_id):
    data = request.get_json()
    return add_comment(blog_id, data, connection)

# PATCH comment by comment id
@app.route("/blogs/<blog_id>/comments/<comment_id>", methods=["PATCH"])
@cross_origin() 
def edit_comment_by_comment_id(blog_id, comment_id):
    data = request.get_json()
    return patch_comment_by_comment_id(blog_id, comment_id, data, connection)

# DELETE comment by comment id
@app.route("/blogs/<blog_id>/comments/<comment_id>", methods=["DELETE"])
@cross_origin() 
def delete_comment_by_comment_id(blog_id, comment_id):
    return remove_comment_by_comment_id(blog_id, comment_id, connection)

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
    return result

# POST conversation by user id
@app.route('/users/<user_id>/conversations', methods=['POST'])
@cross_origin()
def add_conversation_by_user_id(user_id):
    data = request.get_json()
    return add_conversation(user_id, data, connection)

# PATCH conversation by conversation id - doesn't delete, but hides the conversation
@app.route("/conversations/<conversation_id>", methods=["PATCH"])
@cross_origin() 
def delete_conversation_by_conversation_id(conversation_id):
    data = request.get_json()
    return remove_conversation_by_conversation_id(data, conversation_id, connection)

# GET messages by conversation id
@app.route('/conversations/<conversation_id>/messages', methods=['GET'])
@cross_origin()
def get_messages_by_conversation_id(conversation_id):
    result = fetch_messages_by_conversation_id(connection, conversation_id)
    return result

# POST message by conversation id
@app.route('/conversations/<conversation_id>/messages', methods=["POST"])
@cross_origin() 
def add_message_by_conversation_id(conversation_id):
    data = request.get_json()
    return add_message(data, conversation_id, connection)

# POST authenticate user
@app.route('/authenticate', methods=["POST"])
@cross_origin() 
def check_authentication():
    data = request.get_json()
    return authenticate_user(connection, data)

# POST initiate password reset
@app.route('/reset-request', methods=['POST'])
@cross_origin()
def initiate_password_reset():
    data = request.get_json()
    return password_reset_request(data, connection)

# POST set new password
@app.route('/set-new-password', methods=['POST'])
@cross_origin()
def complete_password_reset():
    data = request.get_json()
    return set_new_password(data, connection)

# POST register user
@app.route('/users', methods=['POST'])
@cross_origin()
def register_user():
    data = request.get_json()
    result = add_new_user(data, connection)
    return jsonify(result)

# DELETE user by user id
@app.route("/users/<user_id>", methods=["DELETE"])
@cross_origin() 
def delete_user_by_user_id(user_id):
    return remove_user_by_user_id(user_id, connection)

# PATCH produce by user id
@app.route('/users/<user_id>/produce', methods=["PATCH"])
@cross_origin() 
def patch_user_produce(user_id):
    data = request.get_json()
    produce = data if isinstance(data, list) else []
    return patch_produce_by_user_id(connection, user_id, produce)

# GET all posts
@app.route('/posts', methods=['GET'])
@cross_origin()
def get_all_posts():
    result = fetch_all_posts(connection)
    return result

# POST new post by user id
@app.route('/posts/<user_id>', methods=['POST'])
@cross_origin()
def create_post(user_id):
    data = request.get_json()
    result = add_new_post(data, user_id, connection)
    return jsonify(result)

# DELETE post by post id
@app.route("/posts/<post_id>", methods=["DELETE"])
@cross_origin() 
def delete_post_by_post_id(post_id):
    return remove_post_by_post_id(post_id, connection)

# Handling contact form submissions
@app.route("/contact", methods=["POST"])
@cross_origin() 
def form_submission():
    data = request.get_json()
    return handle_contact_form(data)

# Shopify API route
@app.route('/api/shopify/products', methods=['POST'])
@cross_origin()
def get_shopify_products():
    data = request.get_json()
    return fetch_products(data)

if __name__ == '__main__':
    app.run(debug=True)