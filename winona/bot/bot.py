#!/usr/bin/env python3

import interactions
import os
import dotenv
import atexit


class WinonaBot:
    def __init__(self):
        dotenv.load_dotenv()
        self.TOKEN = os.getenv("BOT_TOKEN")
        self.GUILD_ID = int(os.getenv("GUILD_ID"))
        self.ROLE_ID = int(os.getenv("ROLE_ID"))
        self.ADMIN_CHANNEL_ID = int(os.getenv("ADMIN_CHANNEL_ID"))
        self.DEBUG_GUILD_ID = int(os.getenv("DEBUG_GUILD_ID"))

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

        atexit.register(self.cleanup)

        @self.client.listen()
        async def on_ready():
            print("Bot is ready!")
            return
        return


    def cleanup(self):
        print("Cleaning up...")
        return

    def run(self):
        self.client.start()
        return

def main():
    bot = WinonaBot()
    bot.run()
    return

if __name__ == "__main__":
    main()
