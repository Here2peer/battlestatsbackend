import os

keys = {}
rel_path = 'ApiKeys.cfg'
script_dir = os.path.dirname(__file__)  # <-- absolute dir THIS script is in
with open(os.path.join(script_dir, rel_path), 'r') as f:
#  with open('cfg/ApiKeys.cfg', 'r') as f:
    for line in f:
        (key, value) = line.split(":")
        keys[key] = value

#global url
url = "https://api.developer.battlerite.com/shards/global/"
#global header
header = {
    "Authorization": keys['Battlerite'].strip(),
    "Accept": "application/vnd.api+json"
}
