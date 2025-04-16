#!/usr/bin/env python3

import json
import os
import re
import sys
from ..database import DatabaseManager
from ..database.models.pokemon_species import PokemonSpecies

def load_json(filename):
    data = {}
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
    else:
        raise FileNotFoundError(filename)
    return data

def is_shadow(species):
    species_id = species['speciesId']
    if 'tags' in species:
        tags = species['tags']
    else:
        tags = []
    shadow_by_id = species_id[-7:] == "_shadow"
    shadow_by_tag = "shadow" in tags
    if shadow_by_id != shadow_by_tag:
        print("CONFLICT")
        print("checking if shadow: ", species)
        print("[-7:]: '{}'".format(species_id[-7:]))
        print("tags: {}".format(tags))
    return shadow_by_id

def is_mega(species):
    species_id = species['speciesId']
    if 'tags' in species:
        tags = species['tags']
    else:
        tags = []
    mega_by_id = species_id[-5:] == "_mega"
    mega_by_tag = "mega" in tags
    if mega_by_id != mega_by_tag:
        print("CONFLICT")
        print("checking if mega: ", species)
        print("by_id: '{}'".format(species_id[-5:]))
        print("by_tags: {}".format(tags))
    return mega_by_id

region_list = {'Alolan': {}, 
               'Galarian': {},
               'Hisuian': {},
               'Paldean': {},
               }

def get_form_from_name(species_name):
    matches = re.findall(r'\((.*?)\)', species_name)
    form = ""
    for m in matches:
        if m == 'Shadow': continue
        if m == 'Mega': continue
        if m in region_list: continue
        form = m
        break
    return form

def get_region_from_name(species_name):
    matches = re.findall(r'\((.*?)\)', species_name)
    form = ""
    for m in matches:
        if m in region_list:
            form = m
            break
    return form

def insert_one(dex_entry_json, db_manager):
    print(dex_entry_json)
    name = dex_entry_json['speciesName']
    species_id = dex_entry_json['speciesId']
    dex_number = dex_entry_json['dex']
    region = get_region_from_name(dex_entry_json['speciesName'])
    form = get_form_from_name(dex_entry_json['speciesName'])
    shadow = is_shadow(dex_entry_json) # bool
    mega = is_mega(dex_entry_json)     # bool
    species = PokemonSpecies(name=name, species_id_str=species_id, dex_number=dex_number, region=region, form=form, shadow=shadow, mega=mega)
    db_manager.create_pokemon_species(species)
    return

def insert_all(data, db_manager):
    for entry in data:
        insert_one(entry, db_manager)
    return

def create_pokemon_database(db_file):
    # TODO: This is fragile
    source_json = "./external/pvpoke/src/data/gamemaster/pokemon.json"
    if not os.path.exists(source_json):
        raise FileNotFoundError(source_json)
    try:
        db_manager = DatabaseManager(db_file) 
        # TODO: this needs a big warning, or something.
        db_manager.clear_pokemon_species_table()
        db_manager.drop_pokemon_species_table()

        db_manager.create_pokemon_species_table()
        data = load_json(source_json)
        insert_all(data, db_manager)
    except Exception as e:
        raise e
    finally:
        db_manager.close()
    return

def main(argv):
    db_file = "pokemon_database.db"
    if len(argv) > 1:
        db_file = argv[1]
    create_pokemon_database(db_file)
    return


if __name__ == "__main__":
    main(sys.argv)

#     # print(len(data))
#     # for i in range(7):
#     #     print(data[i])

# for entry in data:
#     name = entry['speciesName']
#     form = get_form_from_name(name)
#     region = get_region_from_name(name)
#     if region:
#         print(name, region)




