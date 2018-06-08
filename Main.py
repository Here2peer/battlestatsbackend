from flask import Flask, redirect, request, jsonify # session?
from flask_openid import OpenID
from flask_cors import cross_origin
from Battlerite.championData import ChampionData
from Battlerite import teams, players, matches
from Steam import Steam

from Database.MongoDB import mongodb
from Database.ORM import champion, tournament

app = Flask(__name__)
openID = OpenID(app)

app.config.update(
    SECRET_KEY = 'static', #os.urandom(24), <-- can be used to use random keys(not api)
    DEBUG = True,
    TESTING = True
)
db = mongodb.initialise_database(app)

@app.route('/dbtest')
def dbtest():
    champion.createChampion('bla', 'bla', 'ucanseeitworks', [], [])
    return champion.getChampion('bla').description


def getInfo(steamID):
    return Steam.getInfo(steamID)

@app.route("/steam", methods = ["GET"])
@openID.loginhandler
def login():
    return openID.try_login('http://steamcommunity.com/openid')

@openID.after_login
def after_login(response):
    #save login
    return redirect(openID.get_next_url())

@app.route("/logout")#add methods?
def logout():
    #pop from session
    return request.referrer #https://stackoverflow.com/questions/14277067/redirect-back-in-flask

@app.route("/allChampionData", methods = ['GET'])
@cross_origin()
def getAllChampionData():
    return ChampionData.get_champion_data() # possibly intergrate with function below

@app.route("/championData/<champion>", methods = ['GET'])
@cross_origin()
def getChampionData(champion):
    return ChampionData.get_champion_data() #work out

@app.route("/tournament/<tournamentID>", methods = ['GET'])
def getTournament():
    return "needs work", 204

@app.route("/tournament/<players>", methods = ["POST"])
def createTournament():
    return "needs work", 204

#-----------------

@app.route('/player')
@cross_origin()
def getPlayer():
    id = 0                              # todo parse args in method
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
    id = 0
    if "id" in request.args.keys():
        if request.args.get('id') == "true":
            id = 1

    if "player" in request.args.keys():
        player_name = request.args.get("player").replace('"', '')
    else:
        player_name = "7854"
        id = 1
    return jsonify(teams.getTeamInfo(id, player_name))
