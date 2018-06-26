import requests

def getInfo(response):
    dataRaw = requests.get(
        "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%s&format=json" % (
        keys['Steam'].strip(), response.identity_url))
    return json.loads(dataRaw.text)['response']['players'][0]
