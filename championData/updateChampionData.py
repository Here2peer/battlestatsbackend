# creates a newgameplay.json with all the data you need

from championData.dataParser.inireader import read_and_convert
from championData.dataParser.jsonreader import combine_json_data

def update_champion_data():
    read_and_convert()
    combine_json_data()

update_champion_data()