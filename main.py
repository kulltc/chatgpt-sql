import logging
from chatgpt import ChatGPT
from google_sql_connector import GoogleCloudSQL
import json
import configparser

# Configure the logging settings
logging.basicConfig(filename='debug.log', filemode='a', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


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

# initialise all the things
google_sql = GoogleCloudSQL(driver, server, database, user, password, encrypt)
connection_result = google_sql.connect()
chatModel = ChatGPT(openai_api_key, openai_org, openai_model)

# Send a message to ChatGPT, this function is recursive. 
# The counter is there to make sure it terminates at some point if ChatGPT keeps chatting to itself :).
def run(message, counter=0):
    if (counter > 4):
        return 'error: too many requests'
    responseString = chatModel.message(message)
    try:
        response = json.loads(responseString[:-1] if responseString.endswith('.') else responseString)
    except ValueError:
        return run("Please repeat that answer but use valid JSON only.", counter + 1)
    match response["recipient"]:
        case "USER": 
            return response["message"]
        case "SERVER":
            match response["action"]:
                case "QUERY":
                    result = google_sql.execute_query(response["message"])
                    return run(result, counter + 1)
                case "SCHEMA":
                    result = google_sql.execute_schema(response["message"])
                    return run(result, counter + 1)
                case _:
                    print('error invalid action')
                    print(response)
        case _:
            print('error, invalid recipient')
            print(response)

def main():
    print("Ask any question about the data. Enter 'q' to quit. Enter 'r' to reset ChatGPT.")
    while True:
        user_input = input("Question: ")
        if user_input.lower() == 'q':
            break
        if user_input == "r":
            chatModel.reset()
            continue
        try:
            result = run(user_input)
            print(f"ChatGPT: {result}")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")

if __name__ == "__main__":
    main()
