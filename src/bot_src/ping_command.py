#!/usr/bin/env python3

import interactions

class PingExtension(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client

    @interactions.slash_command(
        name="ping",
        description="Replies with pong!",
    )
    async def ping(self, ctx: interactions.SlashContext):
        await ctx.send("Pong!")

def setup(client):
    PingExtension(client)
