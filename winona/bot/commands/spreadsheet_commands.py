#!/usr/bin/env python3

import interactions
from .checks import admin_channel_check
from ...logic.sheet_validation import validate_draft_sheet_aux, parse_bans_aux
from ...logic.sheet_validation import parse_picks_aux
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

        
    @interactions.slash_command(
        name="winona",
        description="Winona Bot commands.",
        group_name="sheet",
        group_description="Google Sheet commands.",
        sub_cmd_name="show-player-picks",
        sub_cmd_description="Shows the picks made by the player.",
    )
    @interactions.slash_option(
        name="player_name",
        description="The player's choices to show.",
        opt_type=interactions.OptionType.STRING,
        required=True,
        autocomplete=True,
    )
    @interactions.check(admin_channel_check)
    async def show_player_picks(self, ctx: interactions.SlashContext, player_name: str):
        if ctx.guild is None:
            await ctx.send("This command can only be used in a server.")
            return

        sheet_url = ctx.client.winona.sheet_url
        sheet_df = read_public_google_sheet(sheet_url)
        all_picks, users = parse_picks_aux(sheet_df)
        db_manager = ctx.client.winona.db_manager
        all_pokemon = db_manager.get_all_pokemon_species()

        picks = []
        pick_ids = []
        error_msg = ""
        if player_name in users:
            for key in all_picks:
                item = all_picks[key]
                if item[1] == player_name:
                    picks.append(key)
                    for p in all_pokemon:
                        if p.name.lower() == key.lower():
                            pick_ids.append(p.species_id_str.lower())
        else:
            error_msg = f"{player_name} is not in the list."
            
        embed = interactions.Embed(title=player_name + " picks", color=0x00FF00)
        if error_msg:
            embed.add_field(name = "ERROR:", value = error_msg, inline=False)
        elif len(picks) == 0:
            embed.add_field(name = "MSG:", value = "No picks.", inline=False)
        else:
            i = 1
            for pick in picks:
                embed.add_field(name=f"Pick {i}:", value=f"{pick}", inline=False)
                i += 1
            msg = ""
            for pick_id in pick_ids:
                msg += f"{pick_id}\n"
            embed.add_field(name=f"pvpoke import:", value=f"{msg}", inline=False)

        await ctx.send(embeds=embed)

    @show_player_picks.autocomplete("player_name")
    async def show_player_picks_command_player_autocomplete(self, ctx: interactions.AutocompleteContext):
        sheet_url = ctx.client.winona.sheet_url
        sheet_df = read_public_google_sheet(sheet_url)
        all_picks, users = parse_picks_aux(sheet_df)
        
        current_value = ctx.input_text.lower()
        filtered_users = [
            user for user in users if current_value in user.lower()
        ]
        limited_users = filtered_users[:25]
        choices = [
            { "name": user, "value": user} for user in limited_users
        ]
        await ctx.send(choices=choices)



        
def setup(client: interactions.Client):
    SpreadsheetCommands(client)
