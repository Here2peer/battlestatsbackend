# creates a newgameplay.json with all the data you need
import json

import os

from flask import jsonify

from championData.dataParser.inireader import read_and_convert
from championData.dataParser.jsonreader import combine_json_data


def update_champion_data():
    read_and_convert()
    combine_json_data()

def get_champion_data():
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    # combines the layout of gameplay.json with the data from english.ini
    with open(os.path.join(script_dir, "newgameplay.json"), "r") as gameplay:
        return jsonify(json.load(gameplay)), 200
