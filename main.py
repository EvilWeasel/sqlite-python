import sqlite3
from typing import List

DB_FILE = 'database.db'

# To create an in-memory database:
# in_memory_connection = sqlite3.connect(':memory:')


class Customer:
    def __init__(self, first_name, last_name, email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.email}"

    @staticmethod
    def print_customers_table(customers):
        print()
        print(f"{f'First Name':20} | {f'Last Name':20} | {f'Email':20}")
        print("-" * 65)
        for customer in customers:
            print(f"{customer.first_name:20} | {
                  customer.last_name:20} | {customer.email:20}")
        print()

    @staticmethod
    def customer_tuple_to_list(customers):
        return [Customer(customer[0], customer[1], customer[2]) for customer in customers]


def create_connection(db_file):
    connection = None
    try:
        # Create a connection to the database
        # If the database does not exist, it will be created
        connection = sqlite3.connect(db_file)
        print(f"Connection to {db_file} successful")
    except Exception as e:
        print(f"The error '{e}' occurred")

    return connection


def create_customer_table(connection):
    # A cursor is used to interact with the database
    cursor = connection.cursor()
    # Create a customers table
    # Syntax-Hint: column_name data_type
    #  Datatype names on column definitions are optional. A column definition can consist of just the column name and nothing else.
    # Example - This is valid: CREATE TABLE attribute(name TEXT PRIMARY KEY, value) WITHOUT ROWID;

    # Valid Datatypes in SQLite:
    # - NULL -> NULL Value
    # - INTEGER -> Int of Size 0-8 bytes
    # - REAL -> 8-Byte IEEE Floating Point Number
    # - TEXT -> UTF-8/UTF-16 String
    # - BLOB -> Binary Large Object (Stored exactly as input)

    # The data type of the column is determined by the type affinities of the declared type.
    # The type affinities are TEXT, NUMERIC, INTEGER, REAL, and BLOB.
    # The declared type is the recommended type for the column, but SQLite will store any value in any column regardless of the declared type.
    # One could say that the declared type is just a hint to SQLite that you would like to store values of a particular type in the column. If you put a value of one type into a column with a declared type of a different type, SQLite will attempt to convert the value to the declared type.
    # If SQLite cannot convert the value to the declared type, it will store the value as is, using the declared type.
    cursor.execute('''
        create table if not exists customers (
            first_name text,
            last_name text,
            email text
        );
    ''')
    connection.commit()
    print("Table 'customers' created or already exists")


def create_customer(connection, customer: Customer):
    cursor = connection.cursor()
    print(f"Inserting customer {customer.first_name} {
          customer.last_name} into the database...")
    cursor.execute('''
    insert into customers (first_name, last_name, email)
    values (?, ?, ?)
    ''', (customer.first_name, customer.last_name, customer.email))
    connection.commit()
    print(f"""Customer {customer} added to the database""")


def create_many_customers(connection, customers: List[Customer]):
    cursor = connection.cursor()
    print("Inserting the following customers into the database:")
    for customer in customers:
        print(customer)
    cursor.executemany('''
    insert into customers (first_name, last_name, email)
    values (?, ?, ?)
    ''', [(customer.first_name, customer.last_name, customer.email) for customer in customers])
    # list comprehension is used to create a list of tuples from the list of customers, which are dictionaries
    connection.commit()
    print("Customers added to the database")


def select_all_customers(connection):
    cursor = connection.cursor()
    cursor.execute('select * from customers')
    # fetchone() returns the first row of the result set and also moves the cursor to the next row
    customer = cursor.fetchone()
    print("Fetching the first customer from the database:")
    print(customer)
    # fetchall() returns all rows of the result set
    # in this case, it returns all customers in the database minus the first one, because the cursor is already at the second row
    print("Fetching the rest of customers in the database:")
    customers = cursor.fetchall()
    # cast customers tuple to a list of Customer objects
    customers = Customer.customer_tuple_to_list(customers)
    Customer.print_customers_table(customers)
    print("End of customers")
    # fetchmany(size) returns the next set of rows of the result set, where the size is the number of rows to fetch


def main():
    connection = create_connection(DB_FILE)

    create_customer_table(connection)
    # The execute method can be used to run SQL queries, but does not actually run the query until `.commit()` is called on the connection
    customer = Customer('Tobi', 'Wobi', 'twobi@aol.de')
    # create_customer(connection, customer)

    customers = [
        Customer('Max', 'Mustermann', 'mmuster@aol.de'),
        Customer('Erika', 'Mustermann', 'emuster@aol.de'),
        Customer('Henriette', 'Müller', 'hmüller@aol.de')
    ]

    # create_many_customers(connection, customers)

    select_all_customers(connection)

    # Close the connection to avoid memory leaks and locking the database unnecessarily
    connection.close()


if __name__ == '__main__':
    main()
