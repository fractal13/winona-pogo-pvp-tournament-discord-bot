from ..api import read_public_google_sheet
from ..database import DatabaseManager
from ..database.models.pokemon_species import PokemonSpecies
import pandas as pd

def match_pokemon(possible_pokemon_name, all_pokemon):
    fits = []
    for p in all_pokemon:
        if p.name == possible_pokemon_name:
            fits.append(p.name)
            break
        # if p.name.startswith(possible_pokemon_name):
        #     fits.append("Maybe? " + p.name)
    return fits

def validate_draft_sheet_aux(db_manager, sheet_df):
    all_pokemon = db_manager.get_all_pokemon_species()
    users = sheet_df["Trainer"]
    all_picks = {}
    for column in ["PICK 1", "PICK 2", "PICK 3", "PICK 4", "PICK 5", "PICK 6"]:
        for index, value in sheet_df[column].items():
            if pd.isna(value):
                continue
            result = match_pokemon(value, all_pokemon)
            user_size = 15
            value_size = 20
            if len(result) == 0:
                print(f"{column:6s} {index:4d} {users[index][:user_size]:{user_size}s} {value[:value_size]:{value_size}s} {result} <----------------")
            else:
                if result[0] not in all_picks:
                    all_picks[result[0]] = [index, users[index], column]
                else:
                    print("{} already picked by '{}'. '{}' needs to try again.".format(result[0], all_picks[result[0]], [index, users[index], column]))
                pass
                # print(f"{index:4d} {users[index][:user_size]:{user_size}s} {value[:value_size]:{value_size}s} {result}")
    return

def validate_draft_sheet(db_file, sheet_url):
    df = read_public_google_sheet(sheet_url)
    try:
        db_manager = DatabaseManager(db_file)
        validate_draft_sheet_aux(db_manager, df)
    except FileNotFoundError:
        print(f"Error: Database file not found at {db_file}")
    finally:
        db_manager.close()
    
    return

