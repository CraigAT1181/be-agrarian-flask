import json
import psycopg2
from db.connection import get_connection

def seed_database():

    with open('./db/data/test_data/users.json', 'r') as json_file:
        user_test_data = json.load(json_file)

    with open('./db/data/test_data/produce.json', 'r') as json_file:
        produce_test_data = json.load(json_file)

    with open('./db/data/test_data/conversations.json', 'r') as json_file:
        conversation_test_data = json.load(json_file)

    user_values = []
    user_list = user_test_data['users']
    for user in user_list:
        user_values.append((
            user["user_name"],
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
        user_name VARCHAR(255) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        postcode VARCHAR(255) NOT NULL,
        produce VARCHAR(255)[] NOT NULL
        );
    """
    
    insert_user_data = """
        INSERT INTO users 
        (user_name, email, password, postcode, produce)
        VALUES 
        (%s, %s, %s, %s, %s);
    """    

    produce_values = []
    produce_list = produce_test_data['produce']
    for item in produce_list:
        produce_values.append((
            item["produce_name"],
            item["produce_type"],
            item["produce_icon"]
        ))

    drop_produce_table = """
        DROP TABLE IF EXISTS produce;
    """

    create_produce_table = """
        CREATE TABLE produce (
        produce_id SERIAL PRIMARY KEY,
        produce_name VARCHAR(255) UNIQUE NOT NULL,
        produce_type VARCHAR(255),
        produce_icon VARCHAR(255)
        );
    """

    insert_produce_data = """
        INSERT INTO produce
        (produce_name, produce_type, produce_icon)
        VALUES
        (%s, %s, %s);
    """

    conversation_values = []
    conversation_list = conversation_test_data['conversations']
    for conversation in conversation_list:
        conversation["body"] = json.dumps(conversation["body"])
        conversation_values.append((
            conversation["sender_id"],
            conversation["recipient_id"],
            conversation["body"],
            conversation["created_at"]
        ))
    
    drop_conversations_table = """
        DROP TABLE IF EXISTS conversations;
    """
    
    create_conversations_table = """
        CREATE TABLE conversations (
        conversation_id SERIAL PRIMARY KEY,
        sender_id INT REFERENCES users(user_id) ON DELETE CASCADE,
        recipient_id INT REFERENCES users(user_id) ON DELETE CASCADE,
        body JSON NOT NULL,
        created_at TIMESTAMP DEFAULT NOW(),
        UNIQUE (sender_id, recipient_id)
        );
    """
    
    insert_conversation_data = """
        INSERT INTO conversations 
        (sender_id, recipient_id, body, created_at)
        VALUES 
        (%s, %s, %s, %s);
    """

    db_connection = None
    
    db_connection = get_connection()
    db_connection.autocommit = True

    cursor = db_connection.cursor()

    cursor.execute(drop_conversations_table)
    cursor.execute(create_conversations_table)
    for conversation in conversation_values:
        cursor.execute(insert_conversation_data, conversation)
    
    cursor.execute(drop_users_table)       
    cursor.execute(create_users_table)
    for user in user_values:     
        cursor.execute(insert_user_data, user)

    cursor.execute(drop_produce_table)
    cursor.execute(create_produce_table)
    for item in produce_values:
        cursor.execute(insert_produce_data, item)

    db_connection.close()

    print("Data seeded successfully!")
           
seed_database()