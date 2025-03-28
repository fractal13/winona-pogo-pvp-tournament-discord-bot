#!/usr/bin/env python3

import sqlite3
import sys

class DatabaseManager:
    """
    A class to manage database interactions using SQLite3.
    """

    def __init__(self, db_file):
        """
        Initializes the database connection.

        Args:
            db_file (str): Path to the SQLite database file.
        """
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        return

    def execute(self, sql, params=()):
        """
        Executes an SQL statement.

        Args:
            sql (str): The SQL statement to execute.
            params (tuple): A tuple of parameters to substitute into the SQL statement.

        Returns:
            A list of rows returned by the query, if any.
        """
        self.cursor.execute(sql, params)
        self.conn.commit()
        return self.cursor.fetchall()

    def fetchone(self, sql, params=()):
        """
        Executes an SQL statement and returns the first row.

        Args:
            sql (str): The SQL statement to execute.
            params (tuple): A tuple of parameters to substitute into the SQL statement.

        Returns:
            The first row returned by the query, or None if no rows are found.
        """
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()

    def fetchall(self, sql, params=()):
        """
        Executes an SQL statement and returns the all rows.

        Args:
            sql (str): The SQL statement to execute.
            params (tuple): A tuple of parameters to substitute into the SQL statement.

        Returns:
            A list of rows returned by the query, or empty list if no rows are found.
        """
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def create_table(self, create_table_sql):
        """
        Creates a table in the database.

        Args:
            create_table_sql (str): The SQL statement to create the table.
        """
        self.cursor.execute(create_table_sql)
        self.conn.commit()
        return

    def close(self):
        """
        Closes the database connection.
        """
        self.conn.close()
        return

def main(argv):
    db_manager = DatabaseManager("my_database.db")

    # Create a table named 'demo_users'
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS demo_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE
    );
    """
    db_manager.create_table(create_table_sql)

    # Insert data
    db_manager.execute("INSERT INTO demo_users (name, email) VALUES (?, ?)", ("John Doe", "john.doe@example.com"))

    # Select data
    results = db_manager.execute("SELECT * FROM demo_users")
    for row in results:
        print(row)

    # Select a single row
    user = db_manager.fetchone("SELECT * FROM demo_users WHERE id=1")

    db_manager.close()
    return


if __name__ == "__main__":
    main(sys.argv)
