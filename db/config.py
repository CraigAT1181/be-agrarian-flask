from configparser import ConfigParser
from dotenv import load_dotenv
import os

load_dotenv()

#load_dotenv('.env.production')

def load_db_config(filename='database.ini', section='postgresql'):
    db_config = {}

    # Load DATABASE_URL if available in an environment variable (.env, etc)
    db_url = os.getenv('DATABASE_URL')
    
    if db_url:
        db_config['dsn'] = db_url
        return db_config
    
    #Load other configurations from database.ini
    script_dir = os.path.dirname(__file__)
    filepath = os.path.join(script_dir, filename)

    if os.path.exists(filepath):
        parser = ConfigParser()
        parser.read(filepath)

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

    #Load DATABASE_URL if present in environment variable (eg .env)
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
