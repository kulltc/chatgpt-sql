import logging
from langchain_ai import AI
from langchain_db import sql_query, sql_schema

# Configure the logging settings
logging.basicConfig(filename='debug.log', filemode='a', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    print("Ask any question about the data. Enter 'q' to quit. Enter 'r' to reset ChatGPT.")
    agent = AI(sql_query)
    schema_str = sql_schema('Sales.SalesOrderDetail, Sales.SalesOrderHeader, Person.Address, Person.Person, Production.Product, Production.ProductCategory, Production.ProductSubcategory')
    while True:
        user_input = input("Question: ")
        if user_input.lower() == 'q':
            break
        if user_input == "r":
            #todo: fix this.
            print("not yet implemented")
            continue
        try:
            result = agent.run(user_input, schema_str)
            print(f"ChatGPT: {result}")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to quit.")

if __name__ == "__main__":
    main()
