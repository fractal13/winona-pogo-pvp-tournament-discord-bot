#!/usr/bin/env python3

import interactions
import os
import dotenv
import atexit

import argparse
import sys

from ..database import DatabaseManager
from ..cli.cli import g_sheet_url

def parse_arguments(argv):
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Winona Bot")

    parser.add_argument(
        "--db-file",
        help="Database filename",
        default="winona.db"
    )

    return parser.parse_args(argv)

def getenv_int(token):
    s = os.getenv(token)
    i = -1
    try:
        i = int(s)
    except:
        pass
    return i

def getenv_int_list(token):
    strings = os.getenv(token)
    numbers = []
    for s in strings.split(','):
        i = -1
        try:
            i = int(s)
        except:
            pass
        if i != -1:
            numbers.append(i)
    return numbers

class WinonaBot:
    def __init__(self, args=None):
        if args is not None:
            db_file = args.db_file
            if os.path.exists(db_file):
                self.db_manager = DatabaseManager(db_file)
            else:
                raise Exception(f"{db_file} does not exist.")
        else:
            self.db_manager = None
        self.sheet_url = g_sheet_url

        dotenv.load_dotenv()
        # used in Client constructor
        self.TOKEN = os.getenv("BOT_TOKEN")
        # self.GUILD_ID = getenv_int_list("GUILD_ID")
        # self.ROLE_ID = getenv_int("ROLE_ID")
        # used in admin_check
        self.ADMIN_CHANNEL_IDS = getenv_int_list("ADMIN_CHANNEL_ID")
        # used in Client constructor
        self.DEBUG_GUILD_ID = getenv_int("DEBUG_GUILD_ID")

        if self.DEBUG_GUILD_ID:
            self.client = interactions.Client(token=self.TOKEN, debug_scope=self.DEBUG_GUILD_ID)
        else:
            self.client = interactions.Client(token=self.TOKEN)

        # to access bot from callbacks
        self.client.winona = self

        self.client.load_extension("winona.bot.commands.ping_command")
        self.client.load_extension("winona.bot.commands.list_roles_command")
        self.client.load_extension("winona.bot.commands.tournament_command")
        self.client.load_extension("winona.bot.commands.reload_command")
        self.client.load_extension("winona.bot.commands.list_users_command")
        self.client.load_extension("winona.bot.commands.spreadsheet_commands")


        atexit.register(self.cleanup)

        @self.client.listen()
        async def on_ready():
            print("Bot is ready!")
            print(f'Bot is ready! Logged in as {self.client.user}')
            print('-------------------------')
            print('Currently in these servers:')
            for guild in self.client.guilds:
                print(f'- {guild.name} (ID: {guild.id})')
            print('-------------------------')
            return
        return


    def cleanup(self):
        print("Cleaning up...")
        return

    def run(self):
        self.client.start()
        return

def main(argv):
    args = parse_arguments(argv)
    bot = WinonaBot(args)
    bot.run()
    return

if __name__ == "__main__":
    main(sys.argv[1:])
