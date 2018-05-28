import configparser
import json
import os


def read_and_convert():
    config = configparser.ConfigParser()
    # reads english.ini
    script_dir = os.path.dirname(__file__)  # <-- absolute dir THIS script is in

    rel_path = "data/English.ini"
    with open(os.path.join(script_dir, rel_path), encoding='utf8') as infile:
        # print(infile.read())
        config.read_file(infile)

    # writes key/value pairs from english.ini to english.json
    data = {}
    rel_path = 'data/english.json'
    with open(os.path.join(script_dir, rel_path), 'w') as outfile:
        for each_section in config.sections():
            for (each_key, each_val) in config.items(each_section):
                data[each_key] = each_val
        json.dump(data, outfile)
