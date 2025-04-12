#!/usr/bin/env python3

import sqlite3
import sys

import sqlite3
from typing import List, Optional, Tuple
from .models.user import User
from .models.pokemon_species import PokemonSpecies

class DatabaseManager:
    """
    A class to manage database interactions for all models using SQLite3.
    """

    def __init__(self, db_file):
        """
        Initializes the database connection.

        Args:
            db_file (str): Path to the SQLite database file.
        """
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        return

    def execute(self, sql, params=()):
        """
        Executes an SQL statement.

        Args:
            sql (str): The SQL statement to execute.
            params (tuple): A tuple of parameters to substitute into the SQL statement.
        """
        self.cursor.execute(sql, params)
        self.conn.commit()
        return

    def fetchone(self, sql: str, params: tuple = ()) -> Optional[tuple]:
        """
        Executes an SQL statement and returns the first row as a tuple.

        Args:
            sql (str): The SQL statement to execute.
            params (tuple): A tuple of parameters to substitute into the SQL statement.

        Returns:
            The first row as a tuple, or None if no rows are found.
        """
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()

    def fetchall(self, sql: str, params: tuple = ()) -> List[tuple]:
        """
        Executes an SQL statement and returns all rows as a list of tuples.

        Args:
            sql (str): The SQL statement to execute.
            params (tuple): A tuple of parameters to substitute into the SQL statement.

        Returns:
            A list of tuples, or an empty list if no rows are found.
        """
        self.cursor.execute(sql, params)
        return self.cursor.fetchall()

    def create_table(self, create_table_sql):
        """
        Creates a table in the database.

        Args:
            create_table_sql (str): The SQL statement to create the table.
        """
        self.cursor.execute(create_table_sql)
        self.conn.commit()
        return

    def close(self):
        """
        Closes the database connection.
        """
        self.conn.close()
        return

    # User-specific database operations
    def _map_user(self, row: tuple) -> Optional[User]:
        """
        Helper method to map a database row to a User object.
        """
        if row:
            return User(
                user_id=row[0],
                discord_name=row[1],
                discord_name_in_server=row[2],
                discord_id=row[3],
                pogo_trainer_name=row[4],
                pogo_trainer_code=row[5],
                timezone=row[6]
            )
        return None

    def create_user(self, user: User):
        """
        Creates a new user in the database.

        Args:
            user (User): The User object to create.
        """
        sql = """
        INSERT INTO users (discord_name, discord_name_in_server, discord_id,
                            pogo_trainer_name, pogo_trainer_code, timezone)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (user.discord_name, user.discord_name_in_server, user.discord_id,
                  user.pogo_trainer_name, user.pogo_trainer_code, user.timezone)
        self.execute(sql, params)
        user.user_id = self.cursor.lastrowid  # Update the User object with the new ID
        return


    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieves a User object from the database by ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            A User object if found, otherwise None.
        """
        sql = "SELECT id, discord_name, discord_name_in_server, discord_id, pogo_trainer_name, pogo_trainer_code, timezone FROM users WHERE id = ?"
        row = self.fetchone(sql, (user_id,))
        return self._map_user(row)

    def get_user_by_discord_id(self, discord_id: int) -> Optional[User]:
        """
        Retrieves a User object from the database by Discord ID.

        Args:
            discord_id (int): The Discord ID of the user.

        Returns:
            A User object if found, otherwise None.
        """
        sql = "SELECT id, discord_name, discord_name_in_server, discord_id, pogo_trainer_name, pogo_trainer_code, timezone FROM users WHERE discord_id = ?"
        row = self.fetchone(sql, (discord_id,))
        return self._map_user(row)

    def get_all_users(self) -> List[User]:
        """
        Retrieves all users from the database.

        Returns:
            A list of User objects.
        """
        sql = "SELECT id, discord_name, discord_name_in_server, discord_id, pogo_trainer_name, pogo_trainer_code, timezone FROM users"
        rows = self.fetchall(sql)
        return [self._map_user(row) for row in rows]

    def update_user(self, user: User):
        """
        Updates an existing user in the database.

        Args:
            user (User): The User object to update.
        """
        sql = """
        UPDATE users
        SET discord_name = ?, discord_name_in_server = ?, discord_id = ?,
            pogo_trainer_name = ?, pogo_trainer_code = ?, timezone = ?
        WHERE id = ?
        """
        params = (user.discord_name, user.discord_name_in_server, user.discord_id,
                  user.pogo_trainer_name, user.pogo_trainer_code, user.timezone,
                  user.user_id)
        self.execute(sql, params)
        return

    def delete_user(self, user_id: int):
        """
        Deletes a user from the database by ID.

        Args:
            user_id (int): The ID of the user to delete.
        """
        sql = "DELETE FROM users WHERE id = ?"
        self.execute(sql, (user_id,))
        return

    def create_users_table(self):
        """
        Creates the 'users' table in the database.
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            discord_name TEXT NOT NULL,
            discord_name_in_server TEXT,
            discord_id INTEGER UNIQUE NOT NULL,
            pogo_trainer_name TEXT,
            pogo_trainer_code TEXT,
            timezone TEXT
        );
        """
        self.execute(create_table_sql)
        return

    # PokemonSpecies-specific database operations
    def _map_pokemon_species(self, row: Optional[tuple]) -> Optional[PokemonSpecies]:
        """
        Helper method to map a database row to a PokemonSpecies object.
        """
        if row:
            return PokemonSpecies(
                species_id=row[0],
                name=row[1],
                dex_number=row[2],
                region=row[3],
                form=row[4],
                shadow=bool(row[5]),
                mega=bool(row[6]),
            )
        return

    def create_pokemon_species(self, species: PokemonSpecies):
        """
        Creates a new Pokémon species in the database.

        Args:
            species (PokemonSpecies): The PokemonSpecies object to create.
        """
        sql = """
        INSERT INTO pokemon_species (name, dex_number, region, form, shadow, mega)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (species.name, species.dex_number, species.region, species.form,
                  species.shadow, species.mega)
        self.execute(sql, params)
        species.species_id = self.cursor.lastrowid  # Get the new ID
        return

    def get_pokemon_species_by_dex_number(self, dex_number: int) -> Optional[PokemonSpecies]:
        """
        Retrieves a PokemonSpecies object from the database by Dex number.

        Args:
            dex_number (int): The Pokédex number of the species.

        Returns:
            A PokemonSpecies object if found, otherwise None.
        """
        sql = "SELECT * FROM pokemon_species WHERE dex_number = ?"
        row = self.fetchone(sql, (dex_number,))
        return self._map_pokemon_species(row)

    def get_pokemon_species_by_id(self, species_id: int) -> Optional[PokemonSpecies]:
        """
        Retrieves a PokemonSpecies object from the database by ID.

        Args:
            species_id (int): The ID of the species.

        Returns:
            A PokemonSpecies object if found, otherwise None.
        """
        sql = "SELECT * FROM pokemon_species WHERE id = ?"
        row = self.fetchone(sql, (species_id,))
        return self._map_pokemon_species(row)

    def get_all_pokemon_species(self) -> List[PokemonSpecies]:
        """
        Retrieves all PokemonSpecies objects from the database.

        Returns:
            A list of PokemonSpecies objects.
        """
        sql = "SELECT * FROM pokemon_species"
        rows = self.fetchall(sql)
        return [self._map_pokemon_species(row) for row in rows]

    def get_pokemon_species_dex_numbers(self) -> List[int]:
        """
        Retrieves all PokemonSpecies Dex numbers.

        Returns:
            A list of PokemonSpecies dex numbers.
        """
        sql = "SELECT dex_number FROM pokemon_species"
        rows = self.fetchall(sql)
        return [row[0] for row in rows]

    def get_pokemon_species_ids(self) -> List[int]:
        """
        Retrieves all PokemonSpecies ID numbers.

        Returns:
            A list of PokemonSpecies id numbers.
        """
        sql = "SELECT id FROM pokemon_species"
        rows = self.fetchall(sql)
        return [row[0] for row in rows]

    def update_pokemon_species(self, species: PokemonSpecies):
        """
        Updates an existing Pokémon species in the database.

        Args:
            species (PokemonSpecies): The PokemonSpecies object to update.
        """
        sql = """
        UPDATE pokemon_species
        SET name = ?, dex_number = ?, region = ?, form = ?, shadow = ?, mega = ?
        WHERE id = ?
        """
        params = (species.name, species.dex_number, species.region, species.form,
                  species.shadow, species.mega, species.species_id)
        self.execute(sql, params)
        return

    def delete_pokemon_species(self, species_id: int):
        """
        Deletes a Pokémon species from the database by ID.
        Args:
            species_id:
        """
        sql = "DELETE FROM pokemon_species WHERE id = ?"
        self.execute(sql, (species_id,))
        return
        
    def create_pokemon_species_table(self):
        """
        Creates the 'pokemon_species' table in the database.
        """
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS pokemon_species (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dex_number INTEGER NOT NULL,
            region TEXT,
            form TEXT,
            shadow BOOLEAN DEFAULT 0,
            mega BOOLEAN DEFAULT 0
        );
        """
        self.execute(create_table_sql)
        return
       
    def clear_pokemon_species_table(self):
        """
        Removes all rows from the 'pokemon_species' table.
        """
        sql = "DELETE FROM pokemon_species"
        self.execute(sql)
        return

def main(argv):
    db_manager = DatabaseManager("my_database.db")

    # Create a table named 'demo_users'
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS demo_users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE
    );
    """
    db_manager.create_table(create_table_sql)

    # Insert data
    db_manager.execute("INSERT INTO demo_users (name, email) VALUES (?, ?)", ("John Doe", "john.doe@example.com"))

    # Select data
    results = db_manager.execute("SELECT * FROM demo_users")
    for row in results:
        print(row)

    # Select a single row
    user = db_manager.fetchone("SELECT * FROM demo_users WHERE id=1")

    db_manager.close()
    return


if __name__ == "__main__":
    main(sys.argv)
