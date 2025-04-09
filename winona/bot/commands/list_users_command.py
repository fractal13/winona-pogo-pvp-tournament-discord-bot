#!/usr/bin/env python3

import interactions
from .checks import admin_channel_check

class ListUsersCommands(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client

    @interactions.slash_command(
        name="winona",
        description="Winona Bot commands.",
        group_name="user",
        group_description="User commands.",
        sub_cmd_name="list-users",
        sub_cmd_description="Lists all users.",
    )
    @interactions.check(admin_channel_check)
    async def list_users(self, ctx: interactions.SlashContext):
        if ctx.guild is None:
            await ctx.send("This command can only be used in a server.")
            return

        users = ctx.client.winona.db_manager.get_all_users()

        if not users:
            await ctx.send("No users found in the database.")
            return

        embed = interactions.Embed(title="Users", color=0x00FF00)

        for user in users:
            embed.add_field(name=f"ID: {user.discord_id}", value=f"Info: {user.discord_name_in_server}", inline=False)

        await ctx.send(embeds=embed)

    @interactions.slash_command(
        name="winona",
        description="Winona Bot commands.",
        group_name="user",
        group_description="User commands.",
        sub_cmd_name="discord-user-info",
        sub_cmd_description="Displays information about a specific user.",
    )
    @interactions.slash_option(
        name="user",
        description="The user to display information about.",
        opt_type=interactions.OptionType.USER,
        required=True,
    )
    @interactions.check(admin_channel_check)
    async def discord_user_info(self, ctx: interactions.SlashContext, user: interactions.User):
        """Displays information about a Discord user."""
        embed = interactions.Embed(title=f"User Info: {user.display_name}", color=interactions.Color.from_hsv(2.0, 0.8, 0.8))

        embed.add_field(name="ID", value=str(user.id), inline=False)
        embed.add_field(name="DisplayName", value=user.display_name, inline=False)
        embed.add_field(name="tag", value=user.tag, inline=False)
        embed.add_field(name="Mention", value=user.mention, inline=False)
        embed.add_field(name="Created At", value=str(user.created_at), inline=False)

        user = ctx.client.winona.db_manager.get_user_by_discord_id(int(user.id))
        if user:
            embed.add_field(name="UID", value=user.user_id, inline=False)
            embed.add_field(name="UDN", value=user.discord_name, inline=False)
            embed.add_field(name="UDNIS", value=user.discord_name_in_server, inline=False)
            embed.add_field(name="DID", value=user.discord_id, inline=False)
            embed.add_field(name="PTN", value=user.pogo_trainer_name, inline=False)
            embed.add_field(name="PTC", value=user.pogo_trainer_code, inline=False)
            embed.add_field(name="TZ", value=user.timezone, inline=False)

        await ctx.send(embeds=embed)

def setup(client: interactions.Client):
    ListUsersCommands(client)
