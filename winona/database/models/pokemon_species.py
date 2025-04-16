#!/usr/bin/env python3

from typing import Optional

class PokemonSpecies:
    """
    Represents a Pokémon species with its key attributes.
    """

    def __init__(self,
                 name: str,
                 species_id_str: str,
                 dex_number: int,
                 region: Optional[str] = None,
                 form: Optional[str] = None,
                 shadow: bool = False,
                 mega: bool = False,
                 species_id: Optional[int] = None):
        """
        Initializes a PokemonSpecies object.

        Args:
            name (str): The name of the Pokémon species.
            species_id_str (str): The unique string identifier for the species.
            dex_number (int): The Pokédex number of the species.
            region (str, optional): The region where the Pokémon was first introduced.
                                        Defaults to None.
            form (str, optional): The specific form of the Pokémon. Defaults to None.
            shadow (bool): Indicates whether the Pokémon is a Shadow Pokémon.
                                        Defaults to False.
            mega (bool): Indicates whether the Pokémon is a Mega Pokémon.
                                        Defaults to False.
            species_id (int, optional): The ID of the species in the database.
                                        Defaults to None.
        """
        self.name = name
        self.species_id_str = species_id_str
        self.dex_number = dex_number
        self.region = region
        self.form = form
        self.shadow = shadow
        self.mega = mega
        self.species_id = species_id
        return

    def __repr__(self):
        """
        Returns a string representation of the PokemonSpecies object.
        """
        return f"<PokemonSpecies name='{self.name}' species_id='{self.species_id_str}' dex_number='{self.dex_number}'>"

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
        species_str += f" ({self.species_id_str})"
        return species_str
