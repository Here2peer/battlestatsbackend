keys = {}
with open('cfg/ApiKeys.cfg', 'r') as f:
    for line in f:
        (key, value) = line.split(":")
        keys[key] = value

#global url
url = "https://api.dc01.gamelockerapp.com/shards/global/"
#global header
header = {
    "Authorization": keys['Battlerite'],
    "Accept": "application/vnd.api+json"
}
