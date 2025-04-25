import json
import os

def load_json(filename):
    data = {}
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
    else:
        raise FileNotFoundError(filename)
    return data

def read_dracoviz_data(filename):
    data = load_json(filename)
    for player in data:
        msg = "{}".format(player["name"])
        if len(player["pokemon"]) != 6:
            pmsg = "***"
        else:
            pmsg = " ".join([ "{}".format(p["speciesName"]) for p in player["pokemon"]])
        print(msg + " " + pmsg)
    return
