import json
from db.connection import get_connection

# function to seed database

def seed_database ():
    with open('./db/data/test_data/users.json', 'r') as json_file:
        user_test_data = json.load(json_file)

    with open('./db/data/test_data/produce.json', 'r') as json_file:
        produce_test_data = json.load(json_file)

    user_values = []
    user_list = user_test_data['users']
    for user in user_list:
        user_values.append((
            user["name"],
            user["email"],
            user["password"],
            user["location"],
            user["produce"]
        ))

    drop_users_table = """
        DROP TABLE IF EXISTS users;
    """

    create_users_table = """
        CREATE TABLE users (
        user_id SERIAL PRIMARY KEY,
        name VARCHAR(255) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        location JSONB NOT NULL,
        produce VARCHAR(255)[] NOT NULL
        );
    """

    insert_user_data = """
        INSERT INTO users 
        (name, email, password, location, produce)
        VALUES 
        (%s, %s, %s, %s, %s);
    """

    produce_values = []
    produce_list = produce_test_data['produce']
    for item in produce_list:
        produce_values.append((
            item["name"]
        ))

    drop_produce_table = """
        DROP TABLE IF EXISTS produce;
    """

    create_produce_table = """
        CREATE TABLE produce (
        produce_id SERIAL PRIMARY KEY,
        name VARCHAR(255) UNIQUE NOT NULL,
        );
    """

    insert_produce_data = """
        INSERT INTO produce
        (name)
        VALUES
        (%s);
    """

    db_connection = None
    try:
        db_connection = get_connection()
        # db_connection.autocommit = True

        cursor = db_connection.cursor()

        cursor.execute(drop_users_table)
        db_connection.commit()

        cursor.execute(drop_produce_table)
        db_connection.commit()
        
        cursor.execute(create_users_table)
        db_connection.commit()

        cursor.execute(create_produce_table)
        db_connection.commit()

        cursor.executemany(insert_user_data, user_values)
        db_connection.commit()

        cursor.executemany(insert_produce_data, produce_values)
        db_connection.commit()

        print("Data seeded successfully!")
    
    except Exception as e:
        print("Error:", e)
           
seed_database()