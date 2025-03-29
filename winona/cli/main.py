#!/usr/bin/env python3

from ..database import DatabaseManager
from .create_user_database import create_user_database
from .ingest_pokemon_list import create_pokemon_database

import argparse
import sys

def parse_arguments(argv):
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Winona CLI Tool")

    parser.add_argument(
        "action",
        choices=["create-user-db", "create-pokemon-db", "list-pokemon-by-dex", "list-pokemon-by-id"],
        help="Major action to perform"
    )
    parser.add_argument(
        "--db-file",
        help="Database filename",
        default="winona.db"
    )
    # Add optional arguments specific to list-pokemon-by-dex and list-pokemon-by-id
    parser.add_argument(
        "--dex",
        help="Pokemon dex number",
        type=int
    )
    parser.add_argument(
        "--id",
        help="Pokemon id",
        type=int
    )

    return parser.parse_args(argv)

def main(argv):
    """Main function for the Winona CLI tool."""
    args = parse_arguments(argv)

    action = args.action
    db_file = args.db_file
    dex_number = args.dex
    id_number = args.id

    print(f"Action: {action}")
    print(f"Database file: {db_file}")

    if action == "create-user-db":
        # Your create user database logic here
        print(f"Creating user database: {db_file}")
        create_user_database(db_file)
    elif action == "create-pokemon-db":
        # Your create pokemon database logic here
        print(f"Creating pokemon database: {db_file}")
        create_pokemon_database(db_file)
    elif action == "list-pokemon-by-dex":
        # Your list pokemon by dex logic here
        if dex_number is not None:
            print(f"Listing pokemon by dex: {dex_number} from {db_file}")
        else:
            print("Error: --dex argument is required for list-pokemon-by-dex")
    elif action == "list-pokemon-by-id":
        # Your list pokemon by id logic here
        if id_number is not None:
            print(f"Listing pokemon by id: {id_number} from {db_file}")
        else:
            print("Error: --id argument is required for list-pokemon-by-id")
    else:
        print("Invalid action.")

if __name__ == "__main__":
    main(sys.argv[1:]) # Pass sys.argv[1:] to main()
