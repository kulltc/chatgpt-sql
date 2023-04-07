import pyodbc
import csv
import logging
from tabulate import tabulate
import pandas as pd

from io import StringIO

class GoogleCloudSQL:

    def __init__(self, driver, server, database, user, password, encrypt="yes"):
        self.driver = driver
        self.server = server
        self.database = database
        self.user = user
        self.password = password
        self.encrypt = encrypt

    def connect(self):
        try:
            self.conn = pyodbc.connect(f'DRIVER={{{self.driver}}};SERVER={self.server};DATABASE={self.database};UID={self.user};PWD={self.password};ENCRYPT={self.encrypt}')
            return True
        except Exception as e:
            return str(e)

    def close(self):
        self.conn.close()

    def execute_query(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)

        # Get column names
        columns = [column[0] for column in cursor.description]

        # Fetch rows as a list of tuples
        rows = cursor.fetchall()

        # Convert rows and column names to markdown table using tabulate
        markdown_table = tabulate(rows, headers=columns, tablefmt='pipe')

        return markdown_table

    def process_table_string(self, input_str):
        items = input_str.split(',')
        items = [item.split('.')[-1] for item in items]
        formatted_str = "', '".join(items)
        result = f"'{formatted_str}'"
        return result

    def execute_schema(self, table_list):
        queryPart = self.process_table_string(table_list)
        return self.execute_query(f"SELECT CONCAT(TABLE_SCHEMA, '.', TABLE_NAME, ', ', COLUMN_NAME, ', ', DATA_TYPE) AS 'Table, Column, DataType' FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME IN ({queryPart})")
        