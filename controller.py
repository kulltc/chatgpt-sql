import json
from chatgpt import ChatGPT
from google_sql_connector import GoogleCloudSQL
import configparser

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
        with open('./prompts/sql_agent_message_stack.json') as prompts:
            self.gpt_sql = ChatGPT(openai_api_key, openai_org, openai_model, json.load(prompts))
        with open('./prompts/analyst_agent_message_stack.json') as prompts:
            self.gpt_analyst = ChatGPT(openai_api_key, openai_org, openai_model)


    def reset(self):
        self.gpt_analyst.reset()
        self.gpt_sql.reset()

    def run(self, message, sender, counter=0):
        if (counter > 6):
            return 'error: too many requests'

        responseString = self.gpt_sql.message(message, sender)
        self.gpt_analyst = ChatGPT(openai_api_key, openai_org, openai_model)


        try:
            response = json.loads(responseString[:-1] if responseString.endswith('.') else responseString)
        except ValueError:
            return self.run("Please repeat that answer but use valid JSON only.", "SYSTEM", counter + 1)

        match response["recipient"]:
            case "ANALYST":
                print(f"Asking The Business Analyst!: {response['message']}")
                analystAnswer = self.gpt_analyst.message(response["message"], None)
                print(f"Analyst reponds: {analystAnswer}")
                return self.run(analystAnswer, "ANALYST", counter + 1)
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
