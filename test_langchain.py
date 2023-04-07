from ai_langchain import AI
from database_langchain import sql_query

ai = AI(sql_query=sql_query)

print(ai.run("What is the total revenue in 2013"))