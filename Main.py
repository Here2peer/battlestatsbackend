from flask import Flask, redirect, request, jsonify  # session?
from flask_openid import OpenID
from flask_cors import cross_origin
from Battlerite import teams, players, matches, telemetry
from Steam import Steam

from Database.MongoDB import mongodb
from Database.ORM import champion, tournament, test

app = Flask(__name__)
openID = OpenID(app)

app.config.update(
    SECRET_KEY='static',  # os.urandom(24), <-- can be used to use random keys(not api)
    DEBUG=True,
    TESTING=True
)
db = mongodb.initialise_database(app)


def getInfo(steamID):
    return Steam.getInfo(steamID)


@app.route("/steam", methods=["GET"])
@openID.loginhandler
def login():
    return openID.try_login('http://steamcommunity.com/openid')


@openID.after_login
def after_login(response):
    # save login
    return redirect(openID.get_next_url())


@app.route("/logout")  # add methods?
def logout():
    # pop from session
    return request.referrer  # https://stackoverflow.com/questions/14277067/redirect-back-in-flask


@app.route("/tournament/tournamentList", methods=['GET'])
def getTournaments():
    print(request.args.get('playerID'))
    # TODO: Call to get tournaments list for playerID from database
    return "Ok, playerID is " + request.args.get('playerID'), 200


@app.route('/tournament', methods=['GET'])
def getTournament():
    tourney = jsonify(getTournament(request.args.get('tournamentID')))
    return tourney, 200


@app.route('/tournament/signup', methods=['PUT'])
def addTeam():
    p1 = request.data('p1')
    p2 = request.data('p2')
    p3 = request.data('p3')  # if it exists!!

    tournament.addTeam()


@app.route("/tournament/create", methods=["POST"])
def createTournament():
    pID = request.data('playerID')
    numTeams = request.data('numTeams')
    tournament.createTournament(pID, numTeams)
    return "Operation succesfull", 201


@app.route("/tournaments")
def getTournaments():
    return jsonify({'tournaments': tournament.get_all_tournaments()})


@app.route('/player')
@cross_origin()
def getPlayer():
    id = 0  # todo parse args in method
    if "id" in request.args.keys():
        if request.args.get('id') == "true":
            id = 1

    if "player" in request.args.keys():
        player_name = request.args.get("player").replace('"', '')
    else:
        player_name = "Arkdn"
    return jsonify(players.getPlayerInfo(id, player_name, False))


@app.route('/players')
def allPlauers():
    return jsonify(players.getAllPlayers())


@app.route('/champions')
@cross_origin()
def champions():
    return jsonify(champion.getAllChampions())


@app.route('/champion')
@cross_origin()
def champione():
    return jsonify(champion.getChampion(request.args['champion']))


@app.route('/match')
@cross_origin()
def getMatch():
    if "player" in request.args.keys():
        player_name = request.args.get("player").replace('"', '')
    else:
        player_name = "Arkdn"
    return jsonify(matches.getMatchSummary(player_name))


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


@app.route('/test')
def tests():
    return test.do_test()


@app.route('/telemetry')
@cross_origin()
def getTelemetry():
    return telemetry.getKD()
