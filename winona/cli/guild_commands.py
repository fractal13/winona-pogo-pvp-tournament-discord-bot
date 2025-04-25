#!/usr/bin/env python3

import sqlite3
from ..database import DatabaseManager
from ..database.models.guild import Guild
from typing import Optional, List

def create_guild_database(db_file: str) -> bool:
    """
    Creates the 'guilds' table in the specified SQLite database if it doesn't exist.

    Args:
        db_file: The path to the SQLite database file.
    """
    try:
        db_manager = DatabaseManager(db_file)
        db_manager.create_guild_table()
        print("Guild table created (if it didn't exist).")
        return True
    except sqlite3.Error as e:
        print(f"Error creating guild table: {e}")
        return False
    finally:
        db_manager.close()
    return True

def add_guild(db_file: str, guild_id: int, guild_name: Optional[str]) -> bool:
    """
    Adds a new guild to the database.

    Args:
        db_file: The path to the SQLite database file.
        guild_id: The unique ID of the Discord guild.
        guild_name: The name of the Discord guild (optional).

    Returns:
        True if the guild was added successfully, False otherwise.
    """
    if guild_id is None or guild_id <= 0:
        print("Error: Invalid guild ID.")
        return False
    if guild_name is None or guild_name == "":
        print("Error: Guild name cannot be empty.")
        return False
    try:
        db_manager = DatabaseManager(db_file)
        new_guild = Guild(
            guild_id=guild_id,
            admin_channel_id=0,
            tournament_channel_ids=[],
            guild_name=guild_name
        )
        db_manager.create_guild(new_guild)
        print(f"Guild '{guild_name}' added successfully with ID: {new_guild.guild_id}")
        return True
    except FileNotFoundError:
        print(f"Error: Database file not found at {db_file}")
        return False
    except sqlite3.IntegrityError as e:
        print(f"Error adding guild (likely guild ID already exists): {e}")
        return False
    except sqlite3.Error as e:
        print(f"An SQLite error occurred while adding the guild: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while adding the guild: {e}")
        return False
    finally:
        db_manager.close()
    return False


def remove_guild(db_file: str, guild_id: int) -> bool:
    """
    Removes an existing guild from the database.

    Args:
        db_file: The path to the SQLite database file.
        guild_id: The unique ID of the Discord guild.

    Returns:
        True if the guild was removed successfully, False otherwise.
    """
    if guild_id is None or guild_id <= 0:
        print("Error: Invalid guild ID.")
        return False
    
    try:
        db_manager = DatabaseManager(db_file)
        guild = db_manager.get_guild_by_id(guild_id)
        if guild is None:
            print(f"Error: Guild with ID {guild_id} not found in database.")
            return False
        db_manager.delete_guild(guild_id)
        print(f"Guild '{guild_id}' removed successfully.")
        return True
    except FileNotFoundError:
        print(f"Error: Database file not found at {db_file}")
        return False
    except sqlite3.IntegrityError as e:
        print(f"Error removing guild: {e}")
        return False
    except sqlite3.Error as e:
        print(f"An SQLite error occurred while removing the guild: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while removing the guild: {e}")
        return False
    finally:
        db_manager.close()
    return False


def list_guilds(db_file: str) -> None:
    """
    Lists all guilds currently stored in the database.

    Args:
        db_file: The path to the SQLite database file.
    """
    try:
        db_manager = DatabaseManager(db_file)
        guilds: List[Guild] = db_manager.get_all_guilds()
        if guilds:
            print("\n--- Guild List ---")
            for guild in guilds:
                print(guild)  # Assuming Guild has a well-defined __str__ method
                print("-" * 20)
        else:
            print("No guilds found in the database.")
    except FileNotFoundError:
        print(f"Error: Database file not found at {db_file}")
    except sqlite3.Error as e:
        print(f"An SQLite error occurred while listing guilds: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while listing guilds: {e}")
    finally:
        db_manager.close()
    return

def set_guild_admin_channel_id(db_file: str, guild_id: int, admin_channel_id: int) -> bool:
    """
    Updates the admin channel ID for a guild in the database.

    Args:
        db_file: The path to the SQLite database file.
        guild_id: The unique ID of the Discord guild.
        admin_channel_id: The unique ID of the Discord channel.
    """
    try:
        db_manager = DatabaseManager(db_file)
        guild = db_manager.get_guild_by_id(guild_id)
        guild.admin_channel_id = admin_channel_id
        db_manager.update_guild(guild)
        return True
    except FileNotFoundError:
        print(f"Error: Database file not found at {db_file}")
        return False
    except sqlite3.Error as e:
        print(f"An SQLite error occurred while editing guild: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while editing guild: {e}")
        return False
    finally:
        db_manager.close()
    return False

def add_guild_tournament_channel_id(db_file: str, guild_id: int, channel_id: int) -> bool:
    """
    Adds to the tournament channel list.

    Args:
        db_file: The path to the SQLite database file.
        guild_id: The unique ID of the Discord guild.
        channel_id: The ID of a Discord channel.
    """
    try:
        db_manager = DatabaseManager(db_file)
        guild = db_manager.get_guild_by_id(guild_id)
        if channel_id not in guild.tournament_channel_ids:
            guild.tournament_channel_ids.append(channel_id)
            db_manager.update_guild(guild)
        return True
    except FileNotFoundError:
        print(f"Error: Database file not found at {db_file}")
        return False
    except sqlite3.Error as e:
        print(f"An SQLite error occurred while editing guild: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while editing guild: {e}")
        return False
    finally:
        db_manager.close()
    return False

def remove_guild_tournament_channel_id(db_file: str, guild_id: int, channel_id: int) -> bool:
    """
    Removes from the tournament channel list.

    Args:
        db_file: The path to the SQLite database file.
        guild_id: The unique ID of the Discord guild.
        channel_id: The ID of a Discord channel.
    """
    try:
        db_manager = DatabaseManager(db_file)
        guild = db_manager.get_guild_by_id(guild_id)
        if channel_id in guild.tournament_channel_ids:
            guild.tournament_channel_ids.remove(channel_id)
            db_manager.update_guild(guild)
        return True
    except FileNotFoundError:
        print(f"Error: Database file not found at {db_file}")
        return False
    except sqlite3.Error as e:
        print(f"An SQLite error occurred while editing guild: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred while editing guild: {e}")
        return False
    finally:
        db_manager.close()
    return False
