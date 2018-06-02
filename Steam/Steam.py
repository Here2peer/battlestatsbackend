import requests

def getInfo(steamID):
    data = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%s&format=json"
    % (keys['Steam'], steamID))
    return data.text
