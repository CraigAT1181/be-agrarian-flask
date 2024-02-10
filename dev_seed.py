import json
import psycopg2
from db.connection import get_connection

def seed_dev_db():

    print("Connecting to database with the following settings:")
    print("Host:", get_connection().get_dsn_parameters().get('host'))
    print("Database:", get_connection().get_dsn_parameters().get('dbname'))
    print("User:", get_connection().get_dsn_parameters().get('user'))

    with open('./db/data/test_data/users.json', 'r') as json_file:
        user_test_data = json.load(json_file)

    with open('./db/data/test_data/produce.json', 'r') as json_file:
        produce_test_data = json.load(json_file)

    with open('./db/data/test_data/conversations.json', 'r') as json_file:
        conversation_test_data = json.load(json_file)

    with open('./db/data/test_data/messages.json', 'r') as json_file:
        message_test_data = json.load(json_file)
    
    with open('./db/data/test_data/posts.json', 'r') as json_file:
        post_test_data = json.load(json_file)

    user_values = []
    user_list = user_test_data['users']
    for user in user_list:
        user_values.append((
            user["username"],
            user["email"],
            user["password"],
            user["postcode"],
            user["produce"]
        ))
    
    drop_users_table = """
        DROP TABLE IF EXISTS users CASCADE;
    """
    
    create_users_table = """
        CREATE TABLE users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        postcode VARCHAR(255) NOT NULL,
        produce VARCHAR(255)[] NOT NULL
        );
    """
    
    insert_user_data = """
        INSERT INTO users 
        (username, email, password, postcode, produce)
        VALUES 
        (%s, %s, %s, %s, %s);
    """

    drop_verifications_table = """
        DROP TABLE IF EXISTS verifications;
    """
    
    create_verifications_table = """
        CREATE TABLE verifications (
        verification_id SERIAL PRIMARY KEY,
        user_id INT,
        token VARCHAR(255) UNIQUE NOT NULL,
        verification_type VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP NOT NULL,
        is_used BOOLEAN DEFAULT FALSE,
        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
        );
    """

    produce_values = []
    produce_list = produce_test_data['produce']
    for item in produce_list:
        produce_values.append((
            item["produce_name"],
            item["produce_type"],
            item["produce_icon"],
            item["produce_cat"]
        ))

    drop_produce_table = """
        DROP TABLE IF EXISTS produce;
    """

    create_produce_table = """
        CREATE TABLE produce (
        produce_id SERIAL PRIMARY KEY,
        produce_name VARCHAR(255) NOT NULL,
        produce_type VARCHAR(255),
        produce_icon VARCHAR(255),
        produce_cat VARCHAR(255)[]
        );
    """

    insert_produce_data = """
        INSERT INTO produce
        (produce_name, produce_type, produce_icon, produce_cat)
        VALUES
        (%s, %s, %s, %s);
    """

    conversation_values = []
    conversation_list = conversation_test_data['conversations']
    for conversation in conversation_list:
        conversation_values.append((
            conversation["user1_id"],
            conversation["user2_id"],
            conversation["user1_is_deleted"],
            conversation["user2_is_deleted"],
            conversation["created_at"]
        ))
    
    drop_conversations_table = """
        DROP TABLE IF EXISTS conversations;
    """
    
    create_conversations_table = """
        CREATE TABLE conversations (
        conversation_id SERIAL PRIMARY KEY,
        user1_id INT REFERENCES users(user_id) ON DELETE CASCADE,
        user2_id INT REFERENCES users(user_id) ON DELETE CASCADE,
        user1_is_deleted BOOLEAN DEFAULT FALSE,
        user2_is_deleted BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT NOW(),
        UNIQUE (user1_id, user2_id)
        );
    """
    
    insert_conversation_data = """
        INSERT INTO conversations 
        (user1_id, user2_id, user1_is_deleted, user2_is_deleted, created_at)
        VALUES 
        (%s, %s, %s, %s, %s);
    """

    message_values = []
    message_list = message_test_data['messages']
    for message in message_list:
        message_values.append((
            message["conversation_id"],
            message["sender_id"],
            message["message"],
            message["created_at"]
        ))
    
    drop_messages_table = """
        DROP TABLE IF EXISTS messages;
    """
    
    create_messages_table = """
        CREATE TABLE messages (
        message_id SERIAL PRIMARY KEY,
        conversation_id INT REFERENCES conversations(conversation_id) ON DELETE CASCADE,
        sender_id INT REFERENCES users(user_id) ON DELETE CASCADE,
        message VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT NOW()
        );
    """
    
    insert_message_data = """
        INSERT INTO messages 
        (conversation_id, sender_id, message, created_at)
        VALUES 
        (%s, %s, %s, %s);
    """

    post_values = []
    post_list = post_test_data['posts']
    for post in post_list:
        post_values.append((
            post["user_id"],
            post["status"],
            post["type"],
            post["item"],
            post["image"],
            post["body"],
            post["created_at"]
        ))
    
    drop_posts_table = """
        DROP TABLE IF EXISTS posts CASCADE;
    """
    
    create_posts_table = """
        CREATE TABLE posts (
        post_id SERIAL PRIMARY KEY,
        user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
        status VARCHAR(255) NOT NULL,
        type VARCHAR(255) NOT NULL,
        item VARCHAR(255) NOT NULL,
        image VARCHAR(255),
        body VARCHAR(255),
        created_at TIMESTAMP DEFAULT NOW()
        );
    """
    
    insert_post_data = """
        INSERT INTO posts 
        (user_id, status, type, item, image, body, created_at)
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s);
    """

    db_connection = None
    
    db_connection = get_connection()
    print(db_connection, "CONNECTION")
    db_connection.autocommit = True

    cursor = db_connection.cursor()

    cursor.execute(drop_produce_table)
    cursor.execute(drop_users_table)
    cursor.execute(drop_verifications_table)
    cursor.execute(drop_messages_table)
    cursor.execute(drop_conversations_table)
    cursor.execute(drop_posts_table)

    cursor.execute(create_produce_table)
    for item in produce_values:
        cursor.execute(insert_produce_data, item)

    cursor.execute(create_users_table)
    for user in user_values:     
        cursor.execute(insert_user_data, user)

    cursor.execute(create_verifications_table)

    cursor.execute(create_conversations_table)
    for conversation in conversation_values:
        cursor.execute(insert_conversation_data, conversation)

    cursor.execute(create_messages_table)
    for message in message_values:
        cursor.execute(insert_message_data, message)
    
    cursor.execute(create_posts_table)
    for post in post_values:
        cursor.execute(insert_post_data, post)

    db_connection.close()

    print("Data seeded successfully!")
           
seed_dev_db()