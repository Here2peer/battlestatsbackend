import json
import os
from Database.ORM import champion


# put info from newgameplay.json into database
def convert_champion_data():
    print("keys")
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    # combines the layout of gameplay.json with the data from english.ini
    with open(os.path.join(script_dir, "newgameplay.json"), "r") as gameplay:
        gameplay = json.load(gameplay)
        for character in gameplay['characters']:
            icon = character['icon']
            name = character['name']
            description = character['description']
            ability = 1
            abilities = []
            battlerites = []
            for key, value in character.items():
                if key.startswith('ability'):
                    abilities.append(
                        champion.create_ability(value['icon128'], value['name'], value['description'])
                    )
                elif key.startswith('battlerite'):
                    for br in value:
                        battlerites.append(
                            champion.create_battlerite(br['icon'], br['name'], br['abilitySlot'], br['description'])
                        )
            champion.createChampion(icon, name, description, abilities, battlerites)