# A battlerite description refers to tooltip data in the ability descriptions
def get_battlerite_description_tags(description):
    tag_opened = 0
    tooltip_tag_opened = 0
    ability_tag_opened = 0
    ability_tag_started = 0  # first closing bracket passed?

    tags = []
    current_tag = ["", 0, 0, "tag"]  # string, pos1, pos2, type
    for index, char in enumerate(description):
        if tag_opened == 0:
            if char == "{":
                tag_opened = 1
                current_tag = ["", index, 0, "tag"]
        else:
            if tooltip_tag_opened == 0 and ability_tag_opened == 0:
                if char == '2':
                    ability_tag_opened = 1
                else:
                    tooltip_tag_opened = 1
                    current_tag[0] = char
            else:
                if tooltip_tag_opened == 1:
                    if char == "}":
                        tag_opened = 0
                        tooltip_tag_opened = 0
                        current_tag[2] = index
                        current_tag[3] = "tooltip"
                        tags.append(current_tag)
                    else:
                        current_tag[0] = current_tag[0] + char
                else:  # ability tag opened
                    if ability_tag_started == 0:
                        if char == "}":
                            ability_tag_started = 1
                        else:  # summit's wrong
                            tag_opened = 0
                            ability_tag_opened = 0
                    else:
                        if char == "{":
                            tag_opened = 0
                            ability_tag_opened = 0
                            ability_tag_started = 0
                            current_tag[2] = index+2
                            current_tag[3] = "ability"
                            tags.append(current_tag)
                        else:
                            current_tag[0] = current_tag[0] + char
    return tags


def replace_tooltip(tooltip_tag, description, dictionary, original_string_length):
    replace_string = ""
    pos_offset = len(description) - original_string_length
    pos1 = tooltip_tag[1] + pos_offset
    pos2 = tooltip_tag[2] + pos_offset
    if pos1 != -1 & pos2 != -1:
        while pos1 <= pos2:
            replace_string = replace_string + description[pos1]
            pos1 = pos1 + 1
        for tooltip in dictionary["tooltipData"]:
            if tooltip["Name"].lower() == tooltip_tag[0].lower():
                replacement_string = tooltip["Value"]
                if "percent" in tooltip["UnitType"].lower():
                    replacement_string += "%"
                if "second" in tooltip["UnitType"].lower():
                    replacement_string += "s"
                description = description.replace(replace_string, replacement_string)
                break
        return description


def replace_ability(ability_tag, description, original_string_length):
    replace_string = ""
    pos_offset = len(description) - original_string_length
    pos1 = ability_tag[1] + pos_offset
    pos2 = ability_tag[2] + pos_offset
    if pos1 != -1 & pos2 != -1:
        while pos1 <= pos2:
            replace_string = replace_string + description[pos1]
            pos1 = pos1 + 1
        description = description.replace(replace_string, ability_tag[0], 1)
        return description


def parse_description(description, dictionary):
    tags = get_battlerite_description_tags(description)
    original_string_length = len(description)
    for tag in tags:
        if tag[3] == "tooltip":
            description = replace_tooltip(tag, description, dictionary, original_string_length)
        if tag[3] == "ability":
            description = replace_ability(tag, description, original_string_length)
    return description
