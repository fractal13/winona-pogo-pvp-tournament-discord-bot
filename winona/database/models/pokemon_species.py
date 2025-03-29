#!/usr/bin/env python3

from typing import Optional
from ..database_manager import DatabaseManager
import sys

class PokemonSpecies:
    """
    Represents a Pokémon species with its key attributes.
    """

    def __init__(self, 
                 name: str, 
                 dex_number: int, 
                 region: Optional[str] = None, 
                 form: Optional[str] = None, 
                 shadow: bool = False, 
                 mega: bool = False, 
                 species_id: Optional[int] = None, 
                 db_manager: Optional[DatabaseManager] = None):
        """
        Initializes a PokemonSpecies object.

        Args:
            name (str): The name of the Pokémon species.
            dex_number (int): The Pokédex number of the species.
            region (str, optional): The region where the Pokémon was first introduced. 
                                   Defaults to None.
            form (str, optional): The specific form of the Pokémon. Defaults to None.
            shadow (bool): Indicates whether the Pokémon is a Shadow Pokémon. 
                           Defaults to False.
            meag (bool): Indicates whether the Pokémon is a Mega Pokémon. 
                           Defaults to False.
            species_id (int, optional): The ID of the species in the database. 
                                     Defaults to None.
            db_manager (DatabaseManager, optional): The database manager instance. 
                                     Defaults to None.
        """
        self.name = name
        self.dex_number = dex_number
        self.region = region
        self.form = form
        self.shadow = shadow
        self.mega = mega
        self.species_id = species_id
        self.db_manager = db_manager
        return

    def save(self):
        """
        Saves the Pokémon species data to the database.
        """
        if self.species_id:
            # Update existing species
            sql = """
            UPDATE pokemon_species
            SET name = ?, dex_number = ?, region = ?, form = ?, shadow = ?, mega = ?
            WHERE id = ?
            """
            params = (self.name, self.dex_number, self.region, self.form, 
                      self.shadow, self.mega, self.species_id)
        else:
            # Create new species
            sql = """
            INSERT INTO pokemon_species (name, dex_number, region, form, shadow, mega)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            params = (self.name, self.dex_number, self.region, self.form, self.shadow, self.mega)

        self.db_manager.execute(sql, params)
        if not self.species_id:
            # Get the inserted species ID
            self.species_id = self.db_manager.cursor.lastrowid
        return

    @classmethod
    def get_by_dex_number(cls, dex_number, db_manager):
        """
        Retrieves a PokemonSpecies object from the database by Dex number.

        Args:
            dex_number (int): The Pokédex number of the species.
            db_manager (DatabaseManager): The database manager instance.

        Returns:
            A PokemonSpecies object if found, otherwise None.
        """
        sql = "SELECT * FROM pokemon_species WHERE dex_number = ?"
        row = db_manager.fetchone(sql, (dex_number,))
        if row:
            return cls(*row[1:], species_id=row[0], db_manager=db_manager)
        return None

    @classmethod
    def get_by_id_number(cls, id_number, db_manager):
        """
        Retrieves a PokemonSpecies object from the database by ID number.

        Args:
            id_number (int): The ID number in the database
            db_manager (DatabaseManager): The database manager instance.

        Returns:
            A PokemonSpecies object if found, otherwise None.
        """
        sql = "SELECT * FROM pokemon_species WHERE id = ?"
        row = db_manager.fetchone(sql, (id_number,))
        if row:
            return cls(*row[1:], species_id=row[0], db_manager=db_manager)
        return None

    @classmethod
    def get_dex_numbers(cls, db_manager):
        """
        Retrieves all PokemonSpecies Dex numbers.

        Args:
            db_manager (DatabaseManager): The database manager instance.

        Returns:
            A list of PokemonSpecies dex numbers.
        """
        sql = "SELECT dex_number FROM pokemon_species"
        return [ row[0] for row in db_manager.fetchall(sql) ]

    @classmethod
    def get_id_numbers(cls, db_manager):
        """
        Retrieves all PokemonSpecies ID numbers.

        Args:
            db_manager (DatabaseManager): The database manager instance.

        Returns:
            A list of PokemonSpecies id numbers.
        """
        sql = "SELECT id FROM pokemon_species"
        return [ row[0] for row in db_manager.fetchall(sql) ]

    @classmethod
    def create_pokemon_species_table(cls, db_manager):
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
        db_manager.create_table(create_table_sql)

    def __str__(self):
        """
        Returns a string representation of the PokemonSpecies object.
        """
        species_str = f"{self.name} (Dex #{self.dex_number})"
        if self.region:
            species_str += f" - {self.region}"
        if self.form:
            species_str += f" - {self.form}"
        if self.shadow:
            species_str += " - Shadow"
        if self.mega:
            species_str += " - Mega"
        return species_str

def main(argv):
    db_manager = DatabaseManager("pokemon_database.db") 

    # Create the pokemon_species table
    PokemonSpecies.create_pokemon_species_table(db_manager)

    # Create some PokemonSpecies objects
    bulbasaur = PokemonSpecies("Bulbasaur", 1, "Kanto", db_manager=db_manager)
    charizard = PokemonSpecies("Charizard", 6, "Kanto", db_manager=db_manager)
    mega_charizard_x = PokemonSpecies("Charizard", 6, "Kanto", "Mega X", db_manager=db_manager)
    shadow_mewtwo = PokemonSpecies("Mewtwo", 150, "Kanto", None, True, db_manager=db_manager)

    # Save the PokemonSpecies objects to the database
    bulbasaur.save()
    charizard.save()
    mega_charizard_x.save()
    shadow_mewtwo.save()

    # Retrieve a PokemonSpecies by Dex number
    retrieved_charizard = PokemonSpecies.get_by_dex_number(6, db_manager)
    print(retrieved_charizard) 

    db_manager.close()
    return


# Example usage
if __name__ == "__main__":
    main(sys.argv)
