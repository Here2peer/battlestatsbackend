keys = {}
with open('cfg/ApiKeys.cfg', 'r') as f:
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
