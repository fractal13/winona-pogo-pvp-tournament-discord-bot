#!/usr/bin/env python3

import interactions

class ReloadCommand(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client

    @interactions.slash_command(
        name="winona",
        description="Winona Bot commands.",
        group_name="admin",
        group_description="Admin commands.",
        sub_cmd_name="reload",
        sub_cmd_description="Reloads an extension.",
    )
    @interactions.slash_option(
        name="extension",
        description="The extension to reload.",
        opt_type=interactions.OptionType.STRING,
        required=True,
        choices=[
            interactions.SlashCommandChoice(name="ping", value="ping_command"),
            interactions.SlashCommandChoice(name="list_roles", value="list_roles_command"),
            interactions.SlashCommandChoice(name="tournament", value="tournament_command"),
            interactions.SlashCommandChoice(name="reload", value="reload_command"),
            interactions.SlashCommandChoice(name="users", value="list_users_command"),
            interactions.SlashCommandChoice(name="spreadsheet", value="spreadsheet_commands"),
        ],
    )
    async def reload_command(self, ctx: interactions.SlashContext, extension: str):
        try:
            self.client.reload_extension("winona.bot.commands."+extension)
            await ctx.send(f"Extension '{extension}' reloaded successfully.")
        except Exception as e:
            await ctx.send(f"Failed to reload extension '{extension}': {e}")

def setup(client):
    ReloadCommand(client)
