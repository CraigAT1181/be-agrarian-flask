import json
import psycopg2
from db.connection import get_connection

def seed_dev_db():
    try:
        with get_connection() as db_connection:
            print("Connecting to database with the following settings:")
            print("Host:", db_connection.get_dsn_parameters().get('host'))
            print("Database:", db_connection.get_dsn_parameters().get('dbname'))
            print("User:", db_connection.get_dsn_parameters().get('user'))

            # Set autocommit to False to wrap all operations in a single transaction
            db_connection.autocommit = False

            # Load data from JSON files
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

            with open('./db/data/test_data/ads.json', 'r') as json_file:
                ad_test_data = json.load(json_file)

            with open('./db/data/test_data/blogs.json', 'r') as json_file:
                blog_test_data = json.load(json_file)

            with open('./db/data/test_data/comments.json', 'r') as json_file:
                comment_test_data = json.load(json_file)

            with open('./db/data/test_data/activities.json', 'r') as json_file:
                activity_test_data = json.load(json_file)

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

            produce_values = []
            produce_list = produce_test_data['produce']
            for item in produce_list:
                produce_values.append((
                    item["produce_name"],
                    item["produce_type"],
                    item["produce_icon"],
                    item["produce_cat"]
                ))

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

            message_values = []
            message_list = message_test_data['messages']
            for message in message_list:
                message_values.append((
                    message["conversation_id"],
                    message["sender_id"],
                    message["message"],
                    message["created_at"]
                ))

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

            ad_values = []
            ad_list = ad_test_data['ads']
            for ad in ad_list:
                ad_values.append((
                    ad["image_url"],
                    ad["redirect_url"]
                ))

            blog_values = []
            blog_list = blog_test_data['blogs']
            for blog in blog_list:
                blog_values.append((
                    blog["title"],
                    blog["author_id"],
                    blog["content"],
                    blog["tags"],
                    blog["date_published"],
                    blog["likes"],
                    blog["image_url"]
                ))

            comment_values = []
            comment_list = comment_test_data['comments']
            for comment in comment_list:
                comment_values.append((
                    comment["blog_id"],
                    comment["user_id"],
                    comment["comment"],
                    comment["parent_comment_id"],
                    comment["date_posted"]
                ))

            activity_values = []
            activity_list = activity_test_data['activities']
            for activity in activity_list:
                activity_values.append((
                    activity["user_id"],
                    activity["title"],
                    activity["description"],
                    activity["datetime"],
                    activity["location"],
                    activity["image_url"],
                    activity["created_at"],
                    activity["updated_at"]
                ))

            # Define SQL statements
            sql_commands = [
                "DROP TABLE IF EXISTS activities CASCADE;",
                "DROP TABLE IF EXISTS comments CASCADE;",
                "DROP TABLE IF EXISTS blogs CASCADE;",
                "DROP TABLE IF EXISTS ads CASCADE;",
                "DROP TABLE IF EXISTS posts CASCADE;",
                "DROP TABLE IF EXISTS messages CASCADE;",
                "DROP TABLE IF EXISTS conversations CASCADE;",
                "DROP TABLE IF EXISTS produce CASCADE;",
                "DROP TABLE IF EXISTS users CASCADE;",
                "DROP TABLE IF EXISTS verifications CASCADE;",
            ]

            # Execute DROP TABLE statements
            with db_connection.cursor() as cursor:
                for command in sql_commands:
                    cursor.execute(command)

            # Create tables and insert data
            with db_connection.cursor() as cursor:
 
                # Insert data into users table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id SERIAL PRIMARY KEY,
                        username VARCHAR(255) UNIQUE NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        postcode VARCHAR(255) NOT NULL,
                        produce VARCHAR(255)[] NOT NULL
                    );
                """)
                for user in user_values:
                    cursor.execute("""
                        INSERT INTO users 
                        (username, email, password, postcode, produce)
                        VALUES 
                        (%s, %s, %s, %s, %s);
                    """, user)

                # Insert data into produce table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS produce (
                        produce_id SERIAL PRIMARY KEY,
                        produce_name VARCHAR(255) NOT NULL,
                        produce_type VARCHAR(255),
                        produce_icon VARCHAR(255),
                        produce_cat VARCHAR(255)[]
                    );
                """)
                for produce in produce_values:
                    cursor.execute("""
                        INSERT INTO produce
                        (produce_name, produce_type, produce_icon, produce_cat)
                        VALUES
                        (%s, %s, %s, %s);
                    """, produce)

                # Insert conversation data
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS conversations (
                        conversation_id SERIAL PRIMARY KEY,
                        user1_id INT REFERENCES users(user_id) ON DELETE CASCADE,
                        user2_id INT REFERENCES users(user_id) ON DELETE CASCADE,
                        user1_is_deleted BOOLEAN DEFAULT FALSE,
                        user2_is_deleted BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT NOW(),
                        UNIQUE (user1_id, user2_id)
                    );
                """)
                
                for conversation in conversation_values:
                    cursor.execute("""
                        INSERT INTO conversations 
                        (user1_id, user2_id, user1_is_deleted, user2_is_deleted, created_at)
                        VALUES 
                        (%s, %s, %s, %s, %s);
                    """, conversation)

                # Insert message data
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS messages (
                        message_id SERIAL PRIMARY KEY,
                        conversation_id INT REFERENCES conversations(conversation_id) ON DELETE CASCADE,
                        sender_id INT REFERENCES users(user_id) ON DELETE CASCADE,
                        message VARCHAR(255) NOT NULL,
                        created_at TIMESTAMP DEFAULT NOW()
                    );
                """)
        
                for message in message_values:
                    cursor.execute("""
                        INSERT INTO messages 
                        (conversation_id, sender_id, message, created_at)
                        VALUES 
                        (%s, %s, %s, %s);
                    """, message)

                # Insert post data
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS posts (
                        post_id SERIAL PRIMARY KEY,
                        user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
                        status VARCHAR(255) NOT NULL,
                        type VARCHAR(255) NOT NULL,
                        item VARCHAR(255) NOT NULL,
                        image VARCHAR(255),
                        body VARCHAR(255),
                        created_at TIMESTAMP DEFAULT NOW()
                    );    
                """)
 
                for post in post_values:
                    cursor.execute("""
                        INSERT INTO posts 
                        (user_id, status, type, item, image, body, created_at)
                        VALUES 
                        (%s, %s, %s, %s, %s, %s, %s);
                    """, post)


                # Insert ad data
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ads (
                        ad_id SERIAL PRIMARY KEY,
                        image_url VARCHAR(255) NOT NULL,
                        redirect_url VARCHAR(255)
                    );
                """)

                for ad in ad_values:
                    cursor.execute("""
                        INSERT INTO ads 
                        (image_url, redirect_url)
                        VALUES 
                        (%s, %s);
                    """, ad)
     
                # Insert blog data
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS blogs (
                        blog_id SERIAL PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        author_id INT REFERENCES users(user_id) ON DELETE SET NULL,
                        content TEXT NOT NULL,
                        tags VARCHAR(255)[],
                        date_published DATE DEFAULT CURRENT_DATE,
                        likes INT DEFAULT 0,
                        image_url VARCHAR(255)
                    );
                """)

                for blog in blog_values:
                    cursor.execute("""
                        INSERT INTO blogs 
                        (title, author_id, content, tags, date_published, likes, image_url)
                        VALUES 
                        (%s, %s, %s, %s, %s, %s, %s);
                    """, blog)

                # Insert comments data
                cursor.execute("""
                    CREATE TABLE comments (
                        comment_id SERIAL PRIMARY KEY,
                        blog_id INT REFERENCES blogs(blog_id) ON DELETE CASCADE,
                        user_id INT REFERENCES users(user_id),
                        comment TEXT NOT NULL,
                        parent_comment_id INT REFERENCES comments(comment_id) ON DELETE CASCADE,
                        date_posted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
        
                for comment in comment_values:
                    cursor.execute("""
                        INSERT INTO comments 
                        (blog_id, user_id, comment, parent_comment_id, date_posted)
                        VALUES 
                        (%s, %s, %s, %s, %s);
                    """, comment)

                # Insert activity data
                cursor.execute("""
                    CREATE TABLE activities (
                        activity_id SERIAL PRIMARY KEY,
                        user_id INT REFERENCES users(user_id),
                        title VARCHAR(255) NOT NULL,
                        description TEXT,
                        datetime TIMESTAMP NOT NULL,
                        location VARCHAR(255) NOT NULL,
                        image_url VARCHAR(255),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
        
                for activity in activity_values:
                    cursor.execute("""
                        INSERT INTO activities 
                        (user_id, title, description, datetime, location, image_url, created_at, updated_at)
                        VALUES 
                        (%s, %s, %s, %s, %s, %s, %s, %s);
                    """, activity)
   
                # Insert verification data
                cursor.execute("""
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
                """)

                # Define functions and triggers
                create_update_activity_timestamp_function = """
                CREATE OR REPLACE FUNCTION update_activity_timestamp()
                RETURNS TRIGGER AS $$
                BEGIN
                    NEW.updated_at = CURRENT_TIMESTAMP;
                    RETURN NEW;
                END;
                $$ LANGUAGE plpgsql;
                """

                create_update_activity_timestamp_trigger = """
                CREATE TRIGGER update_activity_timestamp_trigger
                BEFORE UPDATE ON activities
                FOR EACH ROW
                EXECUTE FUNCTION update_activity_timestamp();
                """

                # Create functions and triggers
                cursor.execute(create_update_activity_timestamp_function)
                cursor.execute(create_update_activity_timestamp_trigger)
                
                # Commit the transaction
                db_connection.commit()
                print("Data seeded successfully!")

    except psycopg2.Error as e:
        # Rollback the transaction if an error occurs
        db_connection.rollback()
        print("An error occurred:", e)

seed_dev_db()