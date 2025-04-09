#!/usr/bin/env python3

import sys

from ..database import DatabaseManager
from ..database.models.user import User

def add_user(db_file: str, discord_name: str, discord_name_in_server: str,
             discord_id: int, pogo_trainer_name: str, pogo_trainer_code: str,
             timezone: str):
    """
    Adds a new user to the database.

    Args:
        db_file (str): Path to the SQLite database file.
        discord_name (str): The user's full Discord name.
        discord_name_in_server (str): The user's nickname in the Discord server.
        discord_id (int): The user's Discord ID.
        pogo_trainer_name (str): The user's Pokémon Go trainer name.
        pogo_trainer_code (str): The user's Pokémon Go trainer code.
        timezone (str): The user's preferred timezone.
    """
    db_manager = DatabaseManager(db_file)
    try:
        new_user = User(
            discord_name=discord_name,
            discord_name_in_server=discord_name_in_server,
            discord_id=discord_id,
            pogo_trainer_name=pogo_trainer_name,
            pogo_trainer_code=pogo_trainer_code,
            timezone=timezone
        )
        db_manager.create_user(new_user)
        print(f"User '{discord_name}' added successfully with ID: {new_user.user_id}")
    except FileNotFoundError:
        print(f"Error: Database file not found at {db_file}")
    except sqlite3.IntegrityError as e:
        if "UNIQUE constraint failed: users.discord_id" in str(e):
            print(f"Error: A user with Discord ID '{discord_id}' already exists.")
        else:
            print(f"An integrity error occurred: {e}")
    except Exception as e:
        print(f"An error occurred while adding the user: {e}")
    finally:
        db_manager.close()
    return

def main(argv):
    db_file = "my_database.db"
    if len(argv) > 1:
        db_file = argv[1]
    add_user(db_file, "dn", "dnis", 1, "ptn", "ptc", "tz")
    return

if __name__ == "__main__":
    main(sys.argv)
