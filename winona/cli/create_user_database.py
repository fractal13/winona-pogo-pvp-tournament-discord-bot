#!/usr/bin/env python3

import sys
from ..database import DatabaseManager
from ..database.models.user import User


def create_user_database(db_file):
    """
    Creates the 'users' table in the specified database file.

    Args:
        db_file (str): Path to the SQLite database file.
    """
    db_manager = DatabaseManager(db_file)
    db_manager.create_users_table()
    db_manager.close()
    return

def main(argv):
    db_file = "my_database.db"
    if len(argv) > 1:
        db_file = argv[1]
    create_user_database(db_file)
    return

if __name__ == "__main__":
    main(sys.argv)
