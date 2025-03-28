#!/usr/bin/env python3

import interactions

class PingCommand(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client

    @interactions.slash_command(
        name="winona",
        description="Winona Bot commands.",
        group_name="utility",
        group_description="Utility commands.",
        sub_cmd_name="ping",
        sub_cmd_description="Responds with the bot's latency.",
    )
    async def ping_command(self, ctx: interactions.SlashContext):
        await ctx.send(f"Pong! Latency: {round(self.client.latency, 1)}ms")

def setup(client):
    PingCommands(client)
