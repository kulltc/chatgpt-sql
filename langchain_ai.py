from langchain.agents import Tool
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.utilities import PythonREPL
import configparser
import os
from langchain.prompts import load_prompt

config = configparser.ConfigParser()
config.read("config.ini")

# Access the config values
os.environ["OPENAI_API_KEY"] = config.get("openai", "api_key")

class AI:

    def __init__(self, sql_query):
        self.llm = OpenAI(temperature=0.3, openai_api_key = config.get("openai", "api_key"), model_name=config.get("openai", "model"))
        self.prompt = load_prompt('./db_prompt.yaml')
        self.tools = [
            Tool(
                name="SQL",
                func=sql_query,
                description="Runs a given SQL query and returns response as Markdown"
            ),
            Tool(
                name="Python REPL",
                func= lambda x: PythonREPL().run(x.strip().strip('`')),
                description="""A Python shell. Use this to do math. Input should be a valid python command.
                If you expect output it should be printed out.""",
            )
        ]
        self.agent = initialize_agent(self.tools, self.llm, agent="zero-shot-react-description", verbose=True, max_iterations=config.get("langchain", "max_iterations"))
    
    def run(self, query, schema):
        agent_prompt = self.prompt.format(query=query, schema=schema)
        return self.agent.run(agent_prompt)