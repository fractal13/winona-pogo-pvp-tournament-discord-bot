#!/usr/bin/env python3

import sys
from ..database import DatabaseManager
from ..database.models.user import User


def create_user_database(db_file):
    db_manager = DatabaseManager(db_file)
    User.create_users_table(db_manager)
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
