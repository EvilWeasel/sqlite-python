import sqlite3
from typing import List

DB_FILE = 'database.db'

# To create an in-memory database:
# in_memory_connection = sqlite3.connect(':memory:')


class Customer:
    def __init__(self, first_name, last_name, email, rowid=None):
        self.rowid = rowid
        self.first_name = first_name
        self.last_name = last_name
        self.email = email

    def __str__(self):
        return f"ID: {self.rowid}\t{self.first_name} {self.last_name} {self.email}"

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
    def print_customers_table_with_rowid(customers):
        print()
        print(f"{f'Rowid':5} | {f'First Name':20} | {
              f'Last Name':20} | {f'Email':20}")
        print("-" * 72)
        for customer in customers:
            print(f"{customer.rowid:5} | {customer.first_name:20} | {
                  customer.last_name:20} | {customer.email:20}")
        print()

    @staticmethod
    def customer_tuple_to_list(customers):
        return [Customer(customer[0], customer[1], customer[2]) for customer in customers]

    @staticmethod
    def customer_tuple_to_list_with_rowid(customers):
        # index 0 is the rowid if it is included in the query
        return [Customer(customer[1], customer[2], customer[3], customer[0]) for customer in customers]


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
    added_customer = cursor.execute(
        'select rowid, * from customers where rowid = last_insert_rowid()').fetchone()
    added_customer = Customer(
        added_customer[1], added_customer[2], added_customer[3], added_customer[0])
    print(f"""Customer {added_customer} added to the database""")


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


def select_all_with_rowid(connection):
    cursor = connection.cursor()
    print("Fetching all customers with rowid:")
    cursor.execute('select rowid, * from customers')
    customers = cursor.fetchall()
    customers = Customer.customer_tuple_to_list_with_rowid(customers)
    Customer.print_customers_table_with_rowid(customers)


def select_customer_by_id(connection, id):
    cursor = connection.cursor()
    print(f"Fetching customer with id {id}")
    cursor.execute('select rowid, * from customers where rowid = ?', (id,))
    customer = cursor.fetchone()
    if customer is None:
        print(f"Customer with id {id} not found")
        return
    customer = Customer(customer[1], customer[2], customer[3], customer[0])
    print(f"Customer with id {id}:\n{customer}")


def select_customer_by_lastname(connection, lastname):
    cursor = connection.cursor()
    print(f"Fetching customers with last name {lastname}")
    # other sql comparison operators are also valid, eg. =, <, >, <=, >=, !=
    cursor.execute('select * from customers where last_name = ?', (lastname,))
    customers = cursor.fetchall()
    customers = Customer.customer_tuple_to_list(customers)
    Customer.print_customers_table(customers)


def select_customer_by_aol_email(connection, email):
    cursor = connection.cursor()
    print(f"Fetching customers with email like {email}")
    cursor.execute('select * from customers where email like ?', (email,))
    customers = cursor.fetchall()
    customers = Customer.customer_tuple_to_list(customers)
    Customer.print_customers_table(customers)


def update_customer(connection, customer: Customer):
    cursor = connection.cursor()
    print(f"Updating customer {customer.first_name} {
          customer.last_name} in the database...")
    cursor.execute('''
    update customers set first_name = ?, last_name = ?, email = ?
    where rowid = ?
    ''', (customer.first_name, customer.last_name, customer.email, customer.rowid))
    connection.commit()
    print(f"""Customer {customer} updated in the database""")


def delete_customer(connection, id):
    cursor = connection.cursor()
    print(f"Deleting customer with id {id}")
    cursor.execute('delete from customers where rowid = ?', (id,))
    connection.commit()
    print(f"Customer with id {id} deleted from the database")


def select_ordered_by_lastname(connection):
    cursor = connection.cursor()
    print("Fetching all customers ordered by last name DESC:")
    cursor.execute('select rowid, * from customers order by last_name DESC')
    customers = cursor.fetchall()
    customers = Customer.customer_tuple_to_list_with_rowid(customers)
    Customer.print_customers_table_with_rowid(customers)


def select_where_multiple_conditions(connection):
    cursor = connection.cursor()
    print("Fetching all customers with last_name Mustermann and email starts with e:")
    cursor.execute(
        'select rowid, * from customers where last_name = ? and email like ?', ('Mustermann', 'e%'))
    customers = cursor.fetchall()
    customers = Customer.customer_tuple_to_list_with_rowid(customers)
    Customer.print_customers_table_with_rowid(customers)


def select_with_limit(connection, limit):
    cursor = connection.cursor()
    print(f"Fetching the first {limit} customers:")
    cursor.execute('select rowid, * from customers limit ?', (limit,))
    customers = cursor.fetchall()
    customers = Customer.customer_tuple_to_list_with_rowid(customers)
    Customer.print_customers_table_with_rowid(customers)


def drop_table(connection, table_name):
    cursor = connection.cursor()
    print(f"Dropping table {table_name}...")
    cursor.execute(f"drop table if exists {table_name}")
    connection.commit()
    print(f"Table {table_name} dropped")


def main():
    connection = create_connection(DB_FILE)

    create_customer_table(connection)
    # The execute method can be used to run SQL queries, but does not actually run the query until `.commit()` is called on the connection
    customer = Customer('Tobi', 'Wobi', 'twobi@aol.de')
    create_customer(connection, customer)

    customers = [
        Customer('Max', 'Mustermann', 'mmuster@aol.de'),
        Customer('Erika', 'Mustermann', 'emuster@aol.de'),
        Customer('Henriette', 'Müller', 'hmüller@aol.de'),
        Customer('Erich', 'Schmidt', 'eschmidt@outlook.de'),
        Customer('Angela', 'Schmidt', 'aschmidt@outlook.de'),
    ]

    create_many_customers(connection, customers)

    # just a bunch of select statements to demonstrate the similar functionality to mysql

    select_all_customers(connection)

    select_all_with_rowid(connection)

    # select by last name
    select_customer_by_lastname(connection, 'Mustermann')

    # select by email (like)
    select_customer_by_aol_email(connection, '%aol.de')

    # update a customer
    customer = Customer('Tobias', 'Wehrle', 'twehrle@aol.de', 1)
    update_customer(connection, customer)
    # check if the customer was updated
    select_customer_by_id(connection, 1)

    # delete a customer
    delete_customer(connection, 1)
    # check if the customer was deleted
    select_customer_by_id(connection, 1)

    # order by lastname
    select_ordered_by_lastname(connection)

    # select where multiple conditions
    select_where_multiple_conditions(connection)

    # select with limit
    select_with_limit(connection, 2)

    # drop the table
    drop_table(connection, 'customers')

    # Close the connection to avoid memory leaks and locking the database unnecessarily
    connection.close()


if __name__ == '__main__':
    main()
