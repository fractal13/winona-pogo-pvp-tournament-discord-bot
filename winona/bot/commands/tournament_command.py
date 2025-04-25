#!/usr/bin/env python3

import interactions
from .checks import admin_channel_check

class TournamentCommand(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client
        self.tournaments = {}

    @interactions.slash_command(
        name="winona",
        description="Winona Bot commands.",
        group_name="tournament",
        group_description="Tournament commands.",
        sub_cmd_name="create",
        sub_cmd_description="Create a new tournament.",
    )
    @interactions.slash_option(
        name="name",
        description="The name of the tournament.",
        opt_type=interactions.OptionType.STRING,
        required=True,
    )
    @interactions.slash_option(
        name="players",
        description="The number of players.",
        opt_type=interactions.OptionType.INTEGER,
        required=True,
    )
    @interactions.check(admin_channel_check)
    async def tournament_create(self, ctx: interactions.SlashContext, name: str, players: int):
        tournament_id = len(self.tournaments) + 1
        self.tournaments[tournament_id] = {
            "name": name,
            "players": players,
            "participants": [],
            "draft_status": "not started",
        }
        embed = interactions.Embed(
            title="Tournament Created",
            description=f"Tournament '{name}' created with {players} players.",
            color=0x00FF00,
        )
        await ctx.send(embeds=embed)

    @interactions.slash_command(
        name="winona",
        description="Winona Bot commands.",
        group_name="tournament",
        group_description="Tournament commands.",
        sub_cmd_name="list",
        sub_cmd_description="List current tournaments.",
    )
    @interactions.check(admin_channel_check)
    async def tournament_list(self, ctx: interactions.SlashContext):
        if not self.tournaments:
            await ctx.send("There are no active tournaments.")
            return

        embed = interactions.Embed(title="Current Tournaments", color=0x00FF00)
        for tournament_id, tournament_data in self.tournaments.items():
            embed.add_field(
                name=f"Tournament ID: {tournament_id}",
                value=f"Name: {tournament_data['name']}, Players: {tournament_data['players']}",
                inline=False,
            )

        await ctx.send(embeds=embed)

def setup(client):
    TournamentCommand(client)
