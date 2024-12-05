# SQLite-Python

A simple demo of how to get started with `sqlite3` in `python3`.

You are free to use this code as you please, if it provides some sort of value to you. ^w^

## SQLite vs SQL

### 1. Serverless vs. Server-Based

- **SQLite**: Serverless; it stores the entire database in a single file and requires no setup.
- **MySQL**: Requires a running server process to handle database queries.
  
**SQLite**: Runs immediately without installing or starting any database server.

```python
import sqlite3

conn = sqlite3.connect('example.db')  # Creates/opens a file 'example.db'
cursor = conn.cursor()
cursor.execute('CREATE TABLE test (id INTEGER PRIMARY KEY, value TEXT)')
conn.commit()
conn.close()
```

**MySQL**: You need to install MySQL, start the MySQL server, and connect like this:

```python
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="example_db"
)
cursor = conn.cursor()
cursor.execute("CREATE TABLE test (id INT AUTO_INCREMENT PRIMARY KEY, value VARCHAR(255))")
conn.commit()
conn.close()
```

### 2. Concurrency

- **SQLite**:
    If two processes try to write at the same time, you might see an error like: `database is locked`

- **MySQL**:
    Handles simultaneous writes seamlessly thanks to its client-server architecture.

### 3. Data Types

- **SQLite**: Dynamically typed (uses "type affinity"); columns can store any type unless constrained.
- **MySQL**: Strongly typed; a column’s type is strictly enforced.

**SQLite**: allows `12345` in a `TEXT` column due to type affinity.

```sql
CREATE TABLE test (id INTEGER, value TEXT);
INSERT INTO test (id, value) VALUES (1, 'Hello');  -- Works
INSERT INTO test (id, value) VALUES (2, 12345);   -- Also works!
```

**MySQL**: enforces the type and throws an error if the data type doesn’t match.

```sql
CREATE TABLE test (id INT, value VARCHAR(255));
INSERT INTO test (id, value) VALUES (1, 'Hello');  -- Works
INSERT INTO test (id, value) VALUES (2, 12345);   -- Error!
```

### 4. Features (Advanced Capabilities)

- **SQLite**: Lightweight but lacks some advanced features like replication, stored procedures, or user management.
- **MySQL**: Supports advanced features such as replication, triggers, and stored procedures.
 
**MySQL Stored Procedure**:

```sql
DELIMITER $$
CREATE PROCEDURE GetUsers()
BEGIN
    SELECT * FROM users;
END$$
DELIMITER ;
CALL GetUsers();
```

SQLite doesn’t support stored procedures directly.

### 5. Use Cases

- **SQLite**: Best for lightweight, local, or embedded use cases (e.g., mobile apps, desktop software).
- **MySQL**: Suited for web applications, enterprise-scale software, or projects needing advanced features.

### 6. Security

- **SQLite**: Doesn’t have built-in user management or authentication, but doesn't really need it (except for more modern use-cases provided by `libsql`)
- **MySQL**: Has robust user management with permissions and roles.

**MySQL**:

```sql
CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON database_name.* TO 'newuser'@'localhost';
```

**SQLite**:
    Doesn’t support users or permissions natively; anyone with access to the file can read/write.

### Overview Table

| Feature               | SQLite                              | MySQL                                |
|-----------------------|-------------------------------------|--------------------------------------|
| Server Requirement    | Serverless, file-based             | Requires server setup               |
| Concurrency           | Limited (single writer)            | High concurrency                    |
| Data Types            | Dynamically typed                  | Strictly typed                      |
| Performance           | Faster for small apps              | Better for large-scale apps         |
| Features              | Basic (no stored procedures)       | Advanced features (replication, triggers) |
| Security              | No built-in user management        | User authentication and permissions |
| Use Cases             | Lightweight apps, mobile, desktop  | Enterprise apps, large-scale systems |

## What is libSQL?

`libSQL` is like SQLite’s cool, modern sibling. It takes the lightweight, embedded database we all know and love (SQLite) and adds new features that make it even more flexible. It's basically **SQLite, open-source with extension** for modern apps and edge deployments.

What makes libSQL awesome?

- **Fork of SQLite:** It’s fully compatible with SQLite but isn’t limited by SQLite’s strict governance.  
- **Extensible:** Adds features like async execution, replication, and more.  
- **Modern use cases:** Designed for edge computing, cloud-native apps, and other cutting-edge scenarios.  

If you love SQLite but wish it could work with "edge" use-cases, libSQL is the answer!

## Sources

- [SQLite Databases with Python - freeCodeCamp.org](https://www.youtube.com/watch?v=byHcYRpMgI4)
- [docs.python.org - sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [sqlite.org/docs](https://www.sqlite.org/docs.html)
- [github.com - libsql](https://github.com/tursodatabase/libsql)
