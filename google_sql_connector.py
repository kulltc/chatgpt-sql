import pyodbc
import csv
import logging

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
        print(f'\033[94mExecuting Query:{query}\033[0m')
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            if len(result) == 0:
                result = "0 rows returned"
                logging.debug(result)
                print(f'\033[96m{result}\033[0m')
                return result

            headers = [column[0] for column in cursor.description]
            output = StringIO()
            csv_writer = csv.writer(output)
            csv_writer.writerow(headers)
            csv_writer.writerows(result)
            result = output.getvalue()
            logging.debug(result)
            print(f'\033[96m{result}\033[0m')
            return result
        except Exception as e:
            return str(e)

    def process_table_string(self, input_str):
        items = input_str.split(',')
        if len(items) > 50:
            raise f'Too many rows returned. This returned {items.length} rows, and there are 50 allowed.'
        items = [item.split('.')[-1] for item in items]
        formatted_str = "', '".join(items)
        result = f"'{formatted_str}'"
        return result

    def execute_schema(self, table_list):
        queryPart = self.process_table_string(table_list)
        return f"SELECT CONCAT(TABLE_SCHEMA, '.', TABLE_NAME, ', ', COLUMN_NAME, ', ', DATA_TYPE) AS 'Table, Column, DataType' FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME IN ({queryPart})"
