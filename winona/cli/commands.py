#!/usr/bin/env python3

from ..database import DatabaseManager
from ..database.models.pokemon_species import PokemonSpecies
import sys

def list_all_by_dex_number(db_file):
    db_manager = DatabaseManager(db_file)
    for dex_number in PokemonSpecies.get_dex_numbers(db_manager):
        p = PokemonSpecies.get_by_dex_number(dex_number, db_manager)
        print(dex_number, p)
    db_manager.close()
    return

def list_all_by_id_number(db_file):
    db_manager = DatabaseManager(db_file)
    for id_number in PokemonSpecies.get_id_numbers(db_manager):
        p = PokemonSpecies.get_by_id_number(id_number, db_manager)
        print(id_number, p)
    db_manager.close()
    return


def main(argv):
    db_file = "my_database.db"
    if len(argv) > 1:
        db_file = argv[1]
    list_all_by_id_number(db_file)
    return

if __name__ == "__main__":
    main(sys.argv)
