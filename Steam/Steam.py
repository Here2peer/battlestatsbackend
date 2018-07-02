import requests, json
from Battlerite.players import getPlayerInfo

from cfg.cfg import keys
def getSInfo(response):
    dataRaw = requests.get(
        "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%s&format=json" % (
        keys['Steam'].strip(), response.identity_url))
    res = getPlayerInfo(False, response.identity_url, True)
    return res#['data'][0]['id']
    #return json.loads(dataRaw.text)['response']['players'][0]
