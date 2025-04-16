#!/usr/bin/env python3

import interactions
from .checks import admin_channel_check
from ...logic.sheet_validation import validate_draft_sheet_aux, parse_bans_aux
from ...api import read_public_google_sheet

class SpreadsheetCommands(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client

    @interactions.slash_command(
        name="winona",
        description="Winona Bot commands.",
        group_name="sheet",
        group_description="Google Sheet commands.",
        sub_cmd_name="validate-draft-sheet",
        sub_cmd_description="Checks that picks are legal names and no pick is a duplicate.",
    )
    @interactions.check(admin_channel_check)
    async def validate_draft_sheet(self, ctx: interactions.SlashContext):
        if ctx.guild is None:
            await ctx.send("This command can only be used in a server.")
            return

        sheet_url = ctx.client.winona.sheet_url
        db_manager = ctx.client.winona.db_manager
        sheet_df = read_public_google_sheet(sheet_url)
        ban_messages, all_bans_by_name = parse_bans_aux(db_manager, sheet_df)
        messages = validate_draft_sheet_aux(db_manager, sheet_df)

        embed = interactions.Embed(title="Issues", color=0x00FF00)
        if len(messages) == 0 and len(ban_messages) == 0:
            pass
        else:
            for message in ban_messages:
                embed.add_field(name=f"MSG:", value=f"Info: {message}", inline=False)
            for message in messages:
                embed.add_field(name=f"MSG:", value=f"Info: {message}", inline=False)

        await ctx.send(embeds=embed)


def setup(client: interactions.Client):
    SpreadsheetCommands(client)
