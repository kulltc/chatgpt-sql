import configparser
from google_sql_connector import GoogleCloudSQL

# Read the config file
config = configparser.ConfigParser()
config.read("config.ini")

# Access the config values
driver = config.get("database", "driver")
server = config.get("database", "server")
database = config.get("database", "database")
user = config.get("database", "user")
password = config.get("database", "password")
encrypt = config.get("database", "encrypt")


db = GoogleCloudSQL(driver, server, database, user, password, encrypt)
db.connect()

def sql_query(query):
    return db.execute_query(strip(query, [' ', '`']))

def strip(string, tokens):
    string = string.strip()
    for token in tokens:
        string = string.strip(token)
    return string

def sql_schema(tables):
    return db.execute_schema(tables)
