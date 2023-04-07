import json
from chatgpt import ChatGPT
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
openai_api_key = config.get("openai", "api_key")
openai_org = config.get("openai", "org")
openai_model = config.get("openai", "model")


class Controller:

    def __init__(self):
        # initialise all the things
        self.google_sql = GoogleCloudSQL(driver, server, database, user, password, encrypt)
        self.google_sql.connect()
        self.chatModel = ChatGPT(openai_api_key, openai_org, openai_model)

    def run(self, message, sender, counter=0):
        if (counter > 4):
            return 'error: too many requests'
        responseString = self.chatModel.message(message, sender)
        try:
            response = json.loads(responseString[:-1] if responseString.endswith('.') else responseString)
        except ValueError:
            return self.run("Please repeat that answer but use valid JSON only.", "SYSTEM", counter + 1)
        match response["recipient"]:
            case "USER": 
                return response["message"]
            case "SERVER":
                match response["action"]:
                    case "QUERY":
                        result = self.google_sql.execute_query(response["message"])
                        return self.run(result, None, counter + 1)
                    case "SCHEMA":
                        result = self.google_sql.execute_schema(response["message"])
                        return self.run(result, None, counter + 1)
                    case _:
                        print('error invalid action')
                        print(response)
            case _:
                print('error, invalid recipient')
                print(response)


    def reset(self):
        self.chatModel.reset()
