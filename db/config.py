from configparser import ConfigParser
from dotenv import load_dotenv
import os

load_dotenv()

def load_db_config(filename='database.ini', section='postgresql_development'):
    db_config = {}

    db_url = os.getenv('DATABASE_URL')
    
    if db_url:
        print(db_url, "DBURL<<<<<")
        db_config['dsn'] = db_url
        
        return db_config
    
    script_dir = os.path.dirname(__file__)
    filepath = os.path.join(script_dir, filename)

    if os.path.exists(filepath):
        parser = ConfigParser()
        parser.read(filepath)
        print(parser, "PARSER")
        print(os.getenv('FLASK_ENV'), "FLASK_ENV<<<<<<<<<<")
        if os.getenv('FLASK_ENV') == 'production':
            section = 'postgresql_production'
        elif os.getenv('FLASK_ENV') == 'development':
            section = 'postgresql_development'
        print(section, "SECTION")
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db_config[param[0]] = param[1]
            
            return db_config
    
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    else:
        raise Exception('No database configuration found in either environment variables or {0}'.format(filename))
    

def load_jwt_config(filename='database.ini', section='jwt'):
    jwt_config = {}

    #Obtain SECRET_KEY if present in environment variable (eg .env)
    key = os.getenv('SECRET_KEY')
    if key:
        jwt_config['SECRET_KEY'] = key
        return jwt_config

    script_dir = os.path.dirname(__file__)
    filepath = os.path.join(script_dir, filename)

    if os.path.exists(filepath):
        parser = ConfigParser()
        parser.read(filepath)

        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                jwt_config[param[0]] = param[1]
            return jwt_config
        
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))
        
    else:
        raise Exception('No secret key found in either environment variables or {0}'.format(filename))
