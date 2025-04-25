#!/usr/bin/env python3

import interactions
from .checks import admin_channel_check

class ListRolesCommands(interactions.Extension):
    def __init__(self, client):
        self.client: interactions.Client = client

    @interactions.slash_command(
        name="winona",
        description="Winona Bot commands.",
        group_name="utility",
        group_description="Utility commands.",
        sub_cmd_name="list-roles",
        sub_cmd_description="Lists all visible roles in the guild.",
    )
    @interactions.check(admin_channel_check)
    async def list_roles(self, ctx: interactions.SlashContext):
        if ctx.guild is None:
            await ctx.send("This command can only be used in a server.")
            return

        roles = ctx.guild.roles  # Get all roles in the guild.

        if not roles:
            await ctx.send("This guild has no roles.")
            return

        embed = interactions.Embed(title="Guild Roles", color=0x00FF00)

        for role in roles:
            if not role.default: #Exclude @everyone role.
                embed.add_field(name=role.name, value=f"ID: {role.id}", inline=False)

        await ctx.send(embeds=embed)

    @interactions.slash_command(
        name="winona",
        description="Winona Bot commands.",
        group_name="utility",
        group_description="Utility commands.",
        sub_cmd_name="role-info",
        sub_cmd_description="Displays information about a specific role.",
    )
    @interactions.slash_option(
        name="role",
        description="The role to display information about.",
        opt_type=interactions.OptionType.ROLE,
        required=True,
    )
    @interactions.check(admin_channel_check)
    async def role_info(self, ctx: interactions.SlashContext, role: interactions.Role):
        embed = interactions.Embed(title=f"Role Info: {role.name}", color=role.color)
        embed.add_field(name="ID", value=role.id, inline=False)
        embed.add_field(name="Color", value=str(role.color), inline=False)
        embed.add_field(name="Mentionable", value=str(role.mentionable), inline=False)
        embed.add_field(name="Hoisted", value=str(role.hoist), inline=False)
        embed.add_field(name="Position", value=str(role.position), inline=False)
        embed.add_field(name="Created At", value=str(role.created_at), inline=False)

        members = [member.mention for member in ctx.guild.members if role in member.roles]
        if members:
            embed.add_field(name="Members", value=", ".join(members), inline=False)
        else:
            embed.add_field(name="Members", value="No members in this role.", inline=False)

        await ctx.send(embeds=embed)

def setup(client: interactions.Client):
    ListRolesCommands(client)
