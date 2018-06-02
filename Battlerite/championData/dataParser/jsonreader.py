from Battlerite.championData.dataParser.descriptionParser import parse_description
import json, os

def combine_json_data():
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    newgameplay = []
    # combines the layout of gameplay.json with the data from english.ini
    with open(os.path.join(script_dir, "data/gameplay.json"), "r") as insfile:
        gameplay = json.load(insfile)["characters"]
        with open(os.path.join(script_dir, "data/English.json"), "r") as infile:
            english = json.load(infile)
            for character in gameplay:
                dictionary = {'icon': character['icon'],
                              "name": english[character["name"]],
                              "description": english[character["description"]]}

                for x in range(1, 8):
                    abilityDict = {}
                    abilitystring = "ability" + str(x)
                    abilityDict['icon'] = character[abilitystring]['icon']
                    abilityDict['icon128'] = character[abilitystring]['icon128']
                    abilityDict['name'] = english[character[abilitystring]['name']]
                    abilityDict['tooltipData'] = character[abilitystring]['tooltipData']

                    description = english[character[abilitystring]['description']]
                    description = parse_description(description, abilityDict)
                    removeFromDescription = ["^2", "^-", "\\n"]
                    for string in removeFromDescription:
                        if string in description:
                            description = description.replace(string, "")
                    abilityDict['description'] = description

                    dictionary[abilitystring] = abilityDict

                skills = character["battlerites"]
                battlerites = []
                for battlerite in skills:
                    brdict = {"icon": battlerite["icon"],
                              'name': english[battlerite["name"]],
                              "abilitySlot": battlerite["abilitySlot"],
                              "tooltipData": battlerite["tooltipData"]}

                    # combine tooltips, abilities and descriptions
                    description = english[battlerite["description"]]
                    description = parse_description(description, brdict)

                    removeFromDescription = ["^2", "^-", "\\n"]
                    for string in removeFromDescription:
                        if string in description:
                            description = description.replace(string, "")

                    brdict["description"] = description

                    battlerites.append(brdict)

                dictionary['battlerites'] = battlerites
                newgameplay.append(dictionary)

    newGamePlayJson = {'characters': newgameplay}
    with open("newgameplay.json", "w") as outfile:
        json.dump(newGamePlayJson, outfile)
