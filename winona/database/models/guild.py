#!/usr/bin/env python3

from typing import List, Optional

class Guild:
    """
    Represents a Discord guild.
    """

    def __init__(self, guild_id: int, admin_channel_id: int, tournament_channel_ids: List[int], guild_name: Optional[str] = None):
        self.guild_id = guild_id  # Unique identifier for the guild (Discord's guild ID)
        self.admin_channel_id = admin_channel_id  # Channel ID for administrative purposes within the guild
        self.tournament_channel_ids = tournament_channel_ids  # List of channel IDs where tournament commands are allowed
        self.guild_name = guild_name  # Optional, for convenience (e.g., storing the guild's name)
        return

    def __repr__(self):
         return f"Guild(guild_id={self.guild_id}, admin_channel_id={self.admin_channel_id}, tournament_channel_ids={self.tournament_channel_ids}, guild_name={self.guild_name})"
