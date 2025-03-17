#!/usr/bin/env python3

from pokemon_species import PokemonSpecies
from database_manager import DatabaseManager
import sys

def list_all_by_dex_number(db_manager):
    for dex_number in PokemonSpecies.get_dex_numbers(db_manager):
        p = PokemonSpecies.get_by_dex_number(dex_number, db_manager)
        print(dex_number, p)
    return

def list_all_by_id_number(db_manager):
    for id_number in PokemonSpecies.get_id_numbers(db_manager):
        p = PokemonSpecies.get_by_id_number(id_number, db_manager)
        print(id_number, p)
    return


def main(argv):
    db_name = "my_database.db"
    if len(argv) > 1:
        db_name = argv[1]
    db_manager = DatabaseManager(db_name)
    list_all_by_id_number(db_manager)
    db_manager.close()
    return

if __name__ == "__main__":
    main(sys.argv)
