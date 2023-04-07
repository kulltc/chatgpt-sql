from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import configparser
import os

config = configparser.ConfigParser()
config.read("config.ini")

# Access the config values
os.environ["OPENAI_API_KEY"] = config.get("openai", "api_key")

PROMPT_TEMPLATE = """
You have access to the AdventureWorks database, that you know from your training data
When you are asked to retrieve data, return a SQL query using the following tables:
Sales.SalesOrderDetail, Sales.SalesOrderHeader, Person.Address, Person.Person, 
Production.Product, Production.ProductCategory, Production.ProductSubcategory


###
{query}
"""


class AI:


    def __init__(self, sql_query):
        self.llm = OpenAI(temperature=0.9, openai_api_key = config.get("openai", "api_key"), model_name="gpt-3.5-turbo")
        self.prompt = PromptTemplate(input_variables=["query"], template=PROMPT_TEMPLATE)
        self.tools = [
            Tool(
                name="SQL",
                func=sql_query,
                description="Runs a given SQL query and returns response as CSV"
            )
        ]
        self.agent = initialize_agent(self.tools, self.llm, agent="zero-shot-react-description", verbose=True, max_iterations=2)
    
    def run(self, query):
        agent_prompt = self.prompt.format(query=query)
        return self.agent.run(agent_prompt)