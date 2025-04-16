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
                if result[0] not in all_picks:
                    all_picks[result[0]] = [index, users[index], column]
                else:
                    msg = "{} already picked by '{}'. '{}' needs to try again.".format(result[0], all_picks[result[0]], [index, users[index], column])
                    messages.append(msg)
    return messages

def validate_draft_sheet(db_file, sheet_url):
    df = read_public_google_sheet(sheet_url)
    try:
        db_manager = DatabaseManager(db_file)
        messages = validate_draft_sheet_aux(db_manager, df)
        for m in messages:
            print(m)
    except FileNotFoundError:
        print(f"Error: Database file not found at {db_file}")
    finally:
        db_manager.close()
    
    return

