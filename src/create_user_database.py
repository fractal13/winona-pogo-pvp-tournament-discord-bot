#!/usr/bin/env python3

import sys
from database_manager import DatabaseManager
from user import User

def main(argv):
    db_name = "my_database.db"
    if len(argv) > 1:
        db_name = argv[1]
    db_manager = DatabaseManager(db_name)
    User.create_users_table(db_manager)
    db_manager.close()
    return

if __name__ == "__main__":
    main(sys.argv)
