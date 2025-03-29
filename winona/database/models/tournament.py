#!/usr/bin/env python3

import sqlite3
from typing import Optional
from ..database_manager import DatabaseManager
import sys


class Tournament:
    """
    Represents a tournament with its key attributes.
    """

    def __init__(self, 
                 discord_server_name: str, 
                 discord_server_id: int, 
                 trainer_role_id: int, 
                 tournament_name: str, 
                 tournament_description: str, 
                 cp_cap: int, 
                 round_length: int, 
                 ban_rounds: int, 
                 dracoviz_link: str, 
                 tournament_id: Optional[int] = None, 
                 db_manager: Optional[DatabaseManager] = None):
        """
        Initializes a Tournament object.

        Args:
            discord_server_name (str): The name of the Discord server.
            discord_server_id (int): The ID of the Discord server.
            trainer_role_id (int): The ID of the Discord role for tournament trainers.
            tournament_name (str): The name of the tournament.
            tournament_description (str): A description of the tournament.
            cp_cap (int): The CP cap for the tournament.
            round_length (int): The length of each round in minutes.
            ban_rounds (int): The number of ban rounds in the tournament.
            dracoviz_link (str): The link to the Dracoviz tournament page.
            tournament_id (int, optional): The ID of the tournament in the database. 
                                        Defaults to None.
            db_manager (DatabaseManager, optional): The database manager instance. 
                                        Defaults to None.
        """
        self.discord_server_name = discord_server_name
        self.discord_server_id = discord_server_id
        self.trainer_role_id = trainer_role_id
        self.tournament_name = tournament_name
        self.tournament_description = tournament_description
        self.cp_cap = cp_cap
        self.round_length = round_length
        self.ban_rounds = ban_rounds
        self.dracoviz_link = dracoviz_link
        self.tournament_id = tournament_id
        self.db_manager = db_manager

    def save(self):
        """
        Saves the tournament data to the database.
        """
        if self.tournament_id:
            # Update existing tournament
            sql = """
            UPDATE tournaments 
            SET discord_server_name = ?, discord_server_id = ?, trainer_role_id = ?, 
                tournament_name = ?, tournament_description = ?, cp_cap = ?, 
                round_length = ?, ban_rounds = ?, dracoviz_link = ?
            WHERE id = ?
            """
            params = (self.discord_server_name, self.discord_server_id, 
                      self.trainer_role_id, self.tournament_name, 
                      self.tournament_description, self.cp_cap, 
                      self.round_length, self.ban_rounds, self.dracoviz_link, 
                      self.tournament_id)
        else:
            # Create new tournament
            sql = """
            INSERT INTO tournaments (discord_server_name, discord_server_id, 
                                     trainer_role_id, tournament_name, 
                                     tournament_description, cp_cap, 
                                     round_length, ban_rounds, dracoviz_link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            params = (self.discord_server_name, self.discord_server_id, 
                      self.trainer_role_id, self.tournament_name, 
                      self.tournament_description, self.cp_cap, 
                      self.round_length, self.ban_rounds, self.dracoviz_link)

        self.db_manager.execute(sql, params)
        if not self.tournament_id:
            # Get the inserted tournament ID
            self.tournament_id = self.db_manager.cursor.lastrowid

    @classmethod
    def get_by_server_id(cls, discord_server_id, db_manager):
        """
        Retrieves a Tournament object from the database by Discord server ID.

        Args:
            discord_server_id (int): The ID of the Discord server.
            db_manager (DatabaseManager): The database manager instance.

        Returns:
            A Tournament object if found, otherwise None.
        """
        sql = "SELECT * FROM tournaments WHERE discord_server_id = ?"
        row = db_manager.fetchone(sql, (discord_server_id,))
        if row:
            return cls(*row[1:], tournament_id=row[0], db_manager=db_manager)
        return None

    @classmethod
    def create_tournaments_table(cls, db_manager):
        """
        Creates the 'tournaments' table in the database.
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS tournaments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            discord_server_name TEXT,
            discord_server_id INTEGER NOT NULL,
            trainer_role_id INTEGER,
            tournament_name TEXT,
            tournament_description TEXT,
            cp_cap INTEGER,
            round_length INTEGER,
            ban_rounds INTEGER,
            dracoviz_link TEXT
        );
        """
        db_manager.create_table(create_table_sql)

    def __str__(self):
        """
        Returns a string representation of the Tournament object.
        """
        return f"Tournament: {self.tournament_name} ({self.discord_server_name})"

# Example usage (assuming you have a `DatabaseManager` instance)
def main(argv):
    db_manager = DatabaseManager("my_database.db") 

    # Create the tournaments table
    Tournament.create_tournaments_table(db_manager)

    # Create a Tournament object
    tournament1 = Tournament(
        "My Discord Server", 
        123456789, 
        987654321, 
        "Summer 2024 Classic", 
        "A friendly 3v3 tournament", 
        1500, 
        5, 
        2, 
        "https://dracoviz.com/mytournament", 
        db_manager=db_manager
    )

    # Save the Tournament object to the database
    tournament1.save()

    # Retrieve the tournament by server ID
    retrieved_tournament = Tournament.get_by_server_id(123456789, db_manager)
    print(retrieved_tournament) 

    db_manager.close()
    return

if __name__ == "__main__":
    main(sys.argv)



        
