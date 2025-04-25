#!/usr/bin/env python3


from ..database import DatabaseManager
from .create_user_database import create_user_database
from .list_users import list_users
from .add_user import add_user
from .ingest_pokemon_list import create_pokemon_database
from .google_commands import display_draft_sheet
from ..logic.sheet_validation import validate_draft_sheet
from ..logic.sheet_validation import parse_bans
from ..logic.sheet_validation import show_player_picks
from ..logic.dracoviz_io import read_dracoviz_data
from .guild_commands import create_guild_database, add_guild, remove_guild, list_guilds, set_guild_admin_channel_id, add_guild_tournament_channel_id, remove_guild_tournament_channel_id

import argparse
import sys

g_sheet_url = "https://docs.google.com/spreadsheets/d/1IyUI18bP2hPjsvZhADDYe93q4QACJ97tpbn8P9CwNE0/edit?gid=0#gid=0"

def parse_arguments(argv):
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Winona CLI Tool")

    parser.add_argument(
        "action",
        choices=["create-pokemon-db", "list-pokemon-by-dex", "list-pokemon-by-id", "list-all-pokemon",
                 "create-user-db", "add-user", "list-users",
                 "create-guild-db", "add-guild", "remove-guild", "list-guilds", "set-admin-channel-id", "add-tournament-channel-id", "remove-tournament-channel-id",
                 "display-draft-sheet", "validate-draft-sheet", "parse-bans",
                 "show-player-picks",
                 "show-dracoviz-data"],
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

    parser.add_argument("--discord-name", default="", help="User's Discord name")
    parser.add_argument("--discord-nick", default="", help="User's Discord nickname in server")
    parser.add_argument("--discord-id", default=0, type=int, help="User's Discord ID")
    parser.add_argument("--pogo-name", default="", help="User's PoGo trainer name")
    parser.add_argument("--pogo-code", default="", help="User's PoGo trainer code")
    parser.add_argument("--timezone", default="", help="User's timezone")

    parser.add_argument("--draft-sheet-url", default=g_sheet_url, help="URL to google sheet with draft picks.")
    parser.add_argument("--player-name", default="", help="Player's name in the sheet")
    parser.add_argument("--filename", default="", help="Filename to operate on")

    parser.add_argument("--guild-name", default="", type=str, help="Guild's Discord name")
    parser.add_argument("--guild-id", default=-1, type=int, help="Guild's Discord id")
    parser.add_argument("--channel-id", default=-1, type=int, help="Channel's Discord id")

    return parser.parse_args(argv)

def create_user_database_UI(args):
    db_file = args.db_file
    print(f"Creating user database: {db_file}")
    create_user_database(db_file)
    return

def create_pokemon_database_UI(args):
    db_file = args.db_file
    print(f"Creating pokemon database: {db_file}")
    create_pokemon_database(db_file)
    return

def list_pokemon_by_dex_UI(args):
    dex_number = args.dex
    db_file = args.db_file
    if dex_number is not None:
        print(f"Listing pokemon by dex: {dex_number} from {db_file}")
    else:
        print("Error: --dex argument is required for list-pokemon-by-dex")
        
    return

def list_pokemon_by_id_UI(args):
    id_number = args.id
    db_file = args.db_file
    if id_number is not None:
        print(f"Listing pokemon by id: {id_number} from {db_file}")
    else:
        print("Error: --id argument is required for list-pokemon-by-id")
    return

from .commands import list_all_pokemon

def list_all_pokemon_UI(args):
    db_file = args.db_file
    list_all_pokemon(db_file)
    return

def list_users_UI(args):
    db_file = args.db_file
    list_users(db_file)
    return


def add_user_UI(args):
    db_file = args.db_file
    discord_name = args.discord_name
    discord_nick = args.discord_nick
    discord_id = args.discord_id
    pogo_name = args.pogo_name
    pogo_code = args.pogo_code
    timezone = args.timezone
    add_user(db_file, discord_name, discord_nick, discord_id, pogo_name, pogo_code, timezone)
    return

def display_draft_sheet_UI(args):
    db_file = args.db_file
    sheet_url = args.draft_sheet_url
    display_draft_sheet(sheet_url)
    return

def validate_draft_sheet_UI(args):
    db_file = args.db_file
    sheet_url = args.draft_sheet_url
    validate_draft_sheet(db_file, sheet_url)
    return

def show_player_picks_UI(args):
    db_file = args.db_file
    sheet_url = args.draft_sheet_url
    player_name = args.player_name
    show_player_picks(db_file, sheet_url, player_name)
    return

def parse_bans_UI(args):
    db_file = args.db_file
    sheet_url = args.draft_sheet_url
    parse_bans(db_file, sheet_url)
    return

def show_dracoviz_data_UI(args):
    filename = args.filename
    read_dracoviz_data(filename)
    return


def create_guild_database_UI(args):
    db_file = args.db_file
    create_guild_database(db_file)
    return

def add_guild_UI(args):
    db_file = args.db_file
    guild_name = args.guild_name
    guild_id = args.guild_id
    add_guild(db_file, guild_id, guild_name)
    return

def remove_guild_UI(args):
    db_file = args.db_file
    guild_id = args.guild_id
    remove_guild(db_file, guild_id)
    return

def list_guilds_UI(args):
    db_file = args.db_file
    list_guilds(db_file)
    return

def set_guild_admin_channel_id_UI(args):
    db_file = args.db_file
    guild_id = args.guild_id
    admin_channel_id = args.channel_id
    set_guild_admin_channel_id(db_file, guild_id, admin_channel_id)
    return

def add_guild_tournament_channel_id_UI(args):
    db_file = args.db_file
    guild_id = args.guild_id
    channel_id = args.channel_id
    add_guild_tournament_channel_id(db_file, guild_id, channel_id)
    return

def remove_guild_tournament_channel_id_UI(args):
    db_file = args.db_file
    guild_id = args.guild_id
    channel_id = args.channel_id
    remove_guild_tournament_channel_id(db_file, guild_id, channel_id)
    return

def main(argv):
    """Main function for the Winona CLI tool."""
    args = parse_arguments(argv)
    actions = {
        "create-user-db": create_user_database_UI,
        "create-pokemon-db": create_pokemon_database_UI,
        "list-pokemon-by-dex": list_pokemon_by_dex_UI,
        "list-pokemon-by-id": list_pokemon_by_id_UI,
        "list-all-pokemon": list_all_pokemon_UI,
        "list-users": list_users_UI,
        "add-user": add_user_UI,
        # GUILD-START
        "create-guild-db": create_guild_database_UI,
        "add-guild": add_guild_UI,
        "remove-guild": remove_guild_UI,
        "list-guilds": list_guilds_UI,
        "set-admin-channel-id": set_guild_admin_channel_id_UI,
        "add-tournament-channel-id": add_guild_tournament_channel_id_UI,
        "remove-tournament-channel-id": remove_guild_tournament_channel_id_UI,
        # GUILD-END
        "display-draft-sheet": display_draft_sheet_UI,
        "validate-draft-sheet": validate_draft_sheet_UI,
        "show-player-picks": show_player_picks_UI,
        "parse-bans": parse_bans_UI,
        "show-dracoviz-data": show_dracoviz_data_UI,
    }
    
    action = args.action
    if action in actions:
        func = actions[action]
        if func:
            func(args)
        else:
            print(f"Command: {action} is not implemented yet.")
    else:
        print(f"Command: {action} is not available.")

    return

if __name__ == "__main__":
    main(sys.argv[1:]) # Pass sys.argv[1:] to main()
