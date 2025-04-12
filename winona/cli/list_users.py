#!/usr/bin/env python3

import sys
from ..database import DatabaseManager
from ..database.models.user import User


def list_users(db_file):
    """
    Lists all users from the specified database file.

    Args:
        db_file (str): Path to the SQLite database file.
    """
    try:
        db_manager = DatabaseManager(db_file)
        users = db_manager.get_all_users()
        if users:
            print("\n--- User List ---")
            for user in users:
                print(user)  # Uses the __str__ method of the User class
                print("-" * 20)
        else:
            print("No users found in the database.")
    except FileNotFoundError:
        print(f"Error: Database file not found at {db_file}")
    except Exception as e:
        print(f"An error occurred while listing users: {e}")
    finally:
        db_manager.close()
    return

def main(argv):
    db_file = "my_database.db"
    if len(argv) > 1:
        db_file = argv[1]
    list_users(db_file)
    return

if __name__ == "__main__":
    main(sys.argv)
