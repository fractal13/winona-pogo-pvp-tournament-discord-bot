#!/usr/bin/env python3

import interactions
import os
import dotenv
import atexit


class WinonaBot:
    def __init__(self):
        dotenv.load_dotenv()
        self.TOKEN = os.getenv("BOT_TOKEN")
        self.GUILD_ID = os.getenv("GUILD_ID")
        self.ROLE_ID = os.getenv("ROLE_ID")
        self.DEBUG_GUILD_ID = os.getenv("DEBUG_GUILD_ID")

        if self.DEBUG_GUILD_ID:
            self.client = interactions.Client(token=self.TOKEN, debug_scope=int(self.DEBUG_GUILD_ID))
        else:
            self.client = interactions.Client(token=self.TOKEN)

        self.client.load_extension("winona.bot.commands.ping_command")
        self.client.load_extension("winona.bot.commands.list_roles_command")
        self.client.load_extension("winona.bot.commands.tournament_command")
        self.client.load_extension("winona.bot.commands.reload_command")

        atexit.register(self.cleanup)

        @self.client.listen()
        async def on_ready():
            print("Bot is ready!")
            # command = await self.client.get_application_command(name="list-roles", guild_id=self.GUILD_ID)

            # if command:
            #     permissions = [
            #         interactions.ApplicationCommandPermissions(
            #             id=self.ROLE_ID,
            #             type=interactions.ApplicationCommandPermissionType.ROLE,
            #             permission=True,
            #         ),
            #         interactions.ApplicationCommandPermissions(
            #             id=self.GUILD_ID,
            #             type=interactions.ApplicationCommandPermissionType.ROLE,
            #             permission=False,
            #         ),
            #     ]
            #     await self.client.edit_application_command_permissions(
            #         command_id=command.id,
            #         guild_id=self.GUILD_ID,
            #         permissions=permissions,
            #     )
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
