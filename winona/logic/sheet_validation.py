from ..api import read_public_google_sheet
from ..database import DatabaseManager
from ..database.models.pokemon_species import PokemonSpecies
import pandas as pd

import rapidfuzz

def fuzz_choice(possible, choices):
    return rapidfuzz.process.extractOne(possible, choices, scorer=rapidfuzz.fuzz.token_sort_ratio)

def match_pokemon(possible_pokemon_name, all_pokemon_names):
    best_fit = fuzz_choice(possible_pokemon_name, all_pokemon_names)
    fits = [ best_fit[0] ]
    return fits

def validate_draft_sheet_aux(db_manager, sheet_df):
    ban_messages, all_bans_by_name = parse_bans_aux(db_manager, sheet_df)
    all_pokemon = db_manager.get_all_pokemon_species()
    all_pokemon_names = [p.name for p in all_pokemon]
    users = sheet_df["Trainer"]
    all_picks = {}
    messages = []
    for column in ["PICK 1", "PICK 2", "PICK 3", "PICK 4", "PICK 5", "PICK 6"]:
        for index, value in sheet_df[column].items():
            if pd.isna(value):
                continue
            result = match_pokemon(value, all_pokemon_names)
            user_size = 15
            value_size = 20
            if len(result) == 0:
                msg = f"{column:6s} {index:4d} {users[index][:user_size]:{user_size}s} {value[:value_size]:{value_size}s} {result} <----------------"
                messages.append(msg)
            elif result[0] != value:
                msg = f"{column:6s} {index:4d} {users[index][:user_size]:{user_size}s} {value[:value_size]:{value_size}s} {result} <----------------"
                messages.append(msg)
            else:
                if False:
                    pass
                elif result[0] in all_picks:
                    msg = "{} already picked by '{}'. '{}' needs to try again.".format(result[0], all_picks[result[0]], [index, users[index], column])
                    messages.append(msg)
                elif result[0] in all_bans_by_name:
                    msg = "{} already banned by '{}'. '{}' needs to try again.".format(result[0], all_bans_by_name[result[0]], [index, users[index], column])
                    messages.append(msg)
                else:
                    all_picks[result[0]] = [index, users[index], column]
    return messages

def validate_draft_sheet(db_file, sheet_url):
    df = read_public_google_sheet(sheet_url)
    try:
        db_manager = DatabaseManager(db_file)
        ban_messages, all_bans_by_name = parse_bans_aux(db_manager, df)
        messages = validate_draft_sheet_aux(db_manager, df)
        for m in ban_messages:
            print(m)
        for m in messages:
            print(m)
    except FileNotFoundError:
        print(f"Error: Database file not found at {db_file}")
    finally:
        db_manager.close()
    
    return


def name_or_id_to_dex(value, all_pokemon):
    dex = -1
    for p in all_pokemon:
        if p.name.lower() == value.lower() or p.species_id_str.lower() == value.lower():
            dex = p.dex_number
            break
    return dex

def ban_to_dex_numbers(value, all_pokemon):
    """
    Given cell's entry for the ban column,
    return a list of dex numbers.

    An entry could be a comma separated list of species_id strings.
    Instead of id strings, it could be the name of an unmodified species.
    """
    dexes = []
    for v in value.split(","):
        dex = name_or_id_to_dex(v, all_pokemon)
        if (dex >= 0) and (dex not in dexes):
            dexes.append(dex)
    return dexes

def dexes_to_species_id_strings(dexes, all_pokemon):
    species_id_strings = []
    names = []
    for dex in dexes:
        for p in all_pokemon:
            if p.dex_number == dex:
                species_id_strings.append(p.species_id_str)
                names.append(p.name)
    species_id_strings = sorted(species_id_strings)
    return species_id_strings, names

def parse_bans_aux(db_manager, sheet_df):
    all_pokemon = db_manager.get_all_pokemon_species()
    all_pokemon_names = [p.name for p in all_pokemon]
    users = sheet_df["Trainer"]
    all_bans = {}
    all_bans_by_name = {}
    messages = []
    for column in ["BAN"]:
        # forward
        #for index, value in sheet_df[column].items():
        # reverse
        for index in reversed(sheet_df[column].index):
            value = sheet_df[column].loc[index]
            if pd.isna(value):
                continue

            dexes = ban_to_dex_numbers(value, all_pokemon)
            species_id_strings, species_names = dexes_to_species_id_strings(dexes, all_pokemon)
            species_id_strings_to_names = dict(zip(species_id_strings, species_names))
            best_ban_string = ",".join(species_id_strings)
            current_ban_string = value.lower()
            
            user_size = 15
            value_size = 30
            if False:
                pass
            elif len(dexes) == 0:
                msg = f"{column:6s} {index:4d} {users[index][:user_size]:{user_size}s} {value[:value_size]:{value_size}s}  <------ No match to a pokemon."
                messages.append(msg)
            elif len(dexes) > 1:
                msg = f"{column:6s} {index:4d} {users[index][:user_size]:{user_size}s} {value[:value_size]:{value_size}s}  {best_ban_string} <------ Match too many pokemon."
                messages.append(msg)
            elif best_ban_string != current_ban_string:
                msg = f"{column:6s} {index:4d} {users[index][:user_size]:{user_size}s} {value[:value_size]:{value_size}s}  {best_ban_string} <------ This is better ban string"
                messages.append(msg)
            else:
                for species_id_str in species_id_strings:
                    if species_id_str not in all_bans:
                        
                        all_bans[species_id_str] = [index, users[index], column]
                        all_bans_by_name[species_id_strings_to_names[species_id_str]] = [index, users[index], column]
                    else:
                        msg = "{} already banned by '{}'. '{}' needs to try again.".format(species_id_str, all_bans[species_id_str], [index, users[index], column])
                        messages.append(msg)
    return messages, all_bans_by_name

def parse_bans(db_file, sheet_url):
    df = read_public_google_sheet(sheet_url)
    try:
        db_manager = DatabaseManager(db_file)
        messages, all_bans_by_name = parse_bans_aux(db_manager, df)
        for m in messages:
            print(m)
    except FileNotFoundError:
        print(f"Error: Database file not found at {db_file}")
    finally:
        db_manager.close()
    
    return
