import csv
import os
from datetime import datetime
from typing import NoReturn, Any

import psycopg2
from dotenv import load_dotenv
from psycopg2 import Error

load_dotenv()
user = os.getenv("user_db")
password = os.getenv("password_db")
host = os.getenv("host_db")
port = os.getenv("port_db")
database = os.getenv("database_db")
global connection, cursor


def test_connection() -> NoReturn:
    global connection, cursor
    try:
        # Connect to an existing database
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")
        # Executing a SQL query
        cursor.execute("SELECT version();")
        # Fetch result
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


# test_connection()

def create_table() -> NoReturn:
    global connection, cursor
    try:
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)

        cursor = connection.cursor()
        # SQL query to create a new table
        create_table_query = '''CREATE TABLE transactions
              (ID INT PRIMARY KEY     NOT NULL,
              DATE           TEXT    NOT NULL,
              TRANSACTION         REAL,
              CLIENT    TEXT); '''
        # Execute a command: this creates a new table
        cursor.execute(create_table_query)
        connection.commit()
        print("Table created successfully in PostgreSQL ")

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


# create_table()

def insert_row(table, name_columns, values) -> NoReturn:
    global connection, cursor
    try:
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)

        cursor = connection.cursor()
        # Executing a SQL query to insert data into  table
        # "ID, DATE, TRANSACTION, CLIENT", "1, 'Iphone12', 1100"
        insert_query = """ INSERT INTO transactions ({}) VALUES ({})""".format(name_columns, values)
        cursor.execute(insert_query)
        connection.commit()
        print("1 Record inserted successfully")
        # Fetch result
        cursor.execute("SELECT * from {}".format(table))
        record = cursor.fetchall()
        print("Result ", record)
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


#   insert_row("transactions", "ID, DATE, TRANSACTION, CLIENT", "1, '01/01/22', 1641.24, 000001")

def insert_data(table, file_transactions) -> NoReturn:
    with open(file_transactions) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader, None)
        for transaction in csv_reader:
            name_cols = "ID, DATE, TRANSACTION, CLIENT"
            print(transaction)
            id_operation = transaction[0]
            dates = datetime.strptime(transaction[1], "%d/%m/%y")
            amount = float(transaction[2])
            client = transaction[3]
            values = "{}, '{}', {}, {}".format(id_operation, dates, amount, client)
            try:
                insert_row(table=table, name_columns=name_cols, values=values)
            except (Exception, psycopg2.Error) as error:
                print("Error to insert row: {}".format(values), error)


# insert_data("transactions", "../transactions.csv")

def read_table(table) -> list[tuple[Any, ...]]:
    global connection, cursor
    try:
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)
        cursor = connection.cursor()
        cursor.execute("SELECT * from {}".format(table))
        record = cursor.fetchall()
        type(record)
        return record
    except (Exception, psycopg2.Error) as error:
        print("Error to read table", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


print(read_table("transactions"))
