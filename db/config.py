from configparser import ConfigParser
from dotenv import load_dotenv
import os

load_dotenv()

def load_db_config(filename='database.ini', section='postgresql'):

    script_dir = os.path.dirname(__file__)
    filepath = os.path.join(script_dir, filename)

    parser = ConfigParser()
    parser.read(filepath)

    db_config = {}

    print(filepath, "filepath")

    db_url = os.getenv('DATABASE_URL')
    if db_url:
        db_config['dsn'] = db_url
    elif filepath:
        parser = ConfigParser()
        parser.read(filepath)

        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db_config[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    else:
        raise Exception('No database configuration found.')

    print(db_config)
    return db_config
