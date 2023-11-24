import json
from db.connection import get_connection

# function to seed database

def seed_database():

    with open('./db/data/test_data/users.json', 'r') as json_file:
        user_test_data = json.load(json_file)

    with open('./db/data/test_data/produce.json', 'r') as json_file:
        produce_test_data = json.load(json_file)

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
        DROP TABLE IF EXISTS users;
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
            item["type"]
        ))

    drop_produce_table = """
        DROP TABLE IF EXISTS produce;
    """

    create_produce_table = """
        CREATE TABLE produce (
        produce_id SERIAL PRIMARY KEY,
        produce_name VARCHAR(255) UNIQUE NOT NULL,
        type VARCHAR(255)
        );
    """

    insert_produce_data = """
        INSERT INTO produce
        (produce_name, type)
        VALUES
        (%s, %s);
    """

    db_connection = None
    try:
        db_connection = get_connection()
        db_connection.autocommit = True

        cursor = db_connection.cursor()
        
        cursor.execute(drop_users_table)       
        cursor.execute(create_users_table)
        for user in user_values:     
            cursor.execute(insert_user_data, user)

        cursor.execute(drop_produce_table)
        cursor.execute(create_produce_table)
        for item in produce_values:
            cursor.execute(insert_produce_data, item)

        print("Data seeded successfully!")
    
    except Exception as e:
        print("Error:", e)
           
seed_database()