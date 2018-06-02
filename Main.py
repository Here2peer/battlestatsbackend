from flask import Flask, redirect
from flask_openid import OpenID
from cfg import keys

from flask import Flask,  redirect, request, session, jsonify
from flask_cors import cross_origin
from championData.ChampionData import update_champion_data, get_champion_data
import teams, players, matches, json, requests, urllib3, re

from urllib import parse

app = Flask(__name__)
openID = OpenID(app)
avatar = ''

app.config.update(
    SECRET_KEY = 'static', #os.urandom(24), <-- can be used to use random keys(not api)
    DEBUG = True,
    TESTING = True
)

def getInfo(steamID):
    data = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%s&format=json"
    % (keys['Steam'], steamID))
    return data.text

@app.route("/steamLogin", methods = ["GET"])
@openID.loginhandler
def login():
    return openID.try_login('http://steamcommunity.com/openid')

@openID.after_login
def after_login(response):
    #save loginhandler
    return redirect(openID.get_next_url())

@app.route("/logout")#add methods?
def logout():
    #pop from session
    return request.referrer #https://stackoverflow.com/questions/14277067/redirect-back-in-flask

#-----------------

@app.route("/gameplay")
@cross_origin()
def getGameplayJson():
    return get_champion_data()

# fix all below
@app.route('/player')
@cross_origin()
def getPlayer():
    id = 0
    if "id" in request.args.keys():
        if request.args.get('id') == "true":
            id = 1

    if "player" in request.args.keys():
        player_name = request.args.get("player").replace('"', '')
    else:
        player_name = "Arkdn"
    return jsonify(players.getPlayerInfo(id, player_name))

@app.route('/match')
@cross_origin()
def getMatch():
    if "player" in request.args.keys():
        player_name = request.args.get("player").replace('"', '')
    else:
        player_name = "Arkdn"
    return jsonify(matches.getMatchesInfo(player_name))

@app.route('/team')
@cross_origin()
def getTeam():
    if "player" in request.args.keys():
        player_name = request.args.get("player").replace('"', '')
    else:
        player_name = "Arkdn"
    return jsonify(teams.getTeamInfo(player_name))
