from flask import Flask, session, request, redirect, url_for, g, jsonify
from flask_cors import cross_origin
from flask_openid import OpenID
import flask_cors
from championData.ChampionData import update_champion_data, get_champion_data
import json, requests, os
import teams
import players
import matches

app = Flask(__name__)
#  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
d = {}
with open('ApiKey.txt', 'r') as f:
    for line in f:
        (key, value) = line.split(":")
        d[key] = value
app.config.update(
    SECRET_KEY = os.urandom(24),
    DEBUG = True,
    TESTING = True
)
openID = OpenID(app)
def getInfo():
    data = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%s&format=json" % (d['steam'].strip(), session['ID']))
    #test = json.loads(data.text) <-- convert to python shit called dict
    return data.text

@app.route("/")
def home():
    #if 'ID' in session:
        #return '>%s<' % d['steam']#.strip()
        #return "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%s&format=json" % (d['steam'], session['ID']), 200
        #return 'Logged in as: %s' % json.loads(getInfo())['response']['players'][0]['personaname'], 200
    #return 'Not logged in', 200

    return players.getPlayerJson("Joltz")

@app.route('/login')
@openID.loginhandler
def login():
    return openID.try_login('http://steamcommunity.com/openid')

@openID.after_login
def go(resp):
    #app.config.update(SECRET_KEY =  resp.identity_url.split('/')[-1]) <-- plz dont remove, may com in handy later
    app.secret_key = resp.identity_url.split('/')[-1]
    session['ID'] = app.config['SECRET_KEY']
    return redirect(url_for('home'))

@app.route("/logout")
def logout():
    session.pop('ID', None)
    return redirect(url_for('home'))

@app.route("/gameplay")
@cross_origin()
def getGameplayJson():
    return get_champion_data()

@app.route('/player')
@cross_origin()
def getPlayer():
    return jsonify(players. getPlayerInfo('Joltz'))

@app.route('/team')
@cross_origin()
def getTeam():
    return jsonify()