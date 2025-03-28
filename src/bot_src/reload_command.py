#!/usr/bin/env python3

import interactions

class ReloadExtension(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client

    @interactions.slash_command(
        name="reload",
        description="Reloads an extension.",
    )
    @interactions.slash_option(
        name="extension",
        description="The extension to reload.",
        opt_type=interactions.OptionType.STRING,
        required=True,
        choices=[
            interactions.SlashCommandChoice(name="ping_command", value="ping_command"),
            interactions.SlashCommandChoice(name="tournament_command", value="tournament_command"),
            interactions.SlashCommandChoice(name="reload_command", value="reload_command"),
        ],    
    )
    async def reload_extension(self, ctx: interactions.SlashContext, extension: str):
        try:
            self.client.reload_extension(extension)
            await ctx.send(f"Extension '{extension}' reloaded successfully.")
        except Exception as e:
            await ctx.send(f"Failed to reload extension '{extension}': {e}")

def setup(client):
    ReloadExtension(client)
