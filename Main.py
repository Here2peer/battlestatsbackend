from flask import Flask, session, redirect, url_for, jsonify, request, g, make_response
from flask_openid import OpenID
from flask_cors import cross_origin
import json, requests, os

app = Flask(__name__)
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

@app.route("/steamuser")
def getInfo():
    if 'steamID' in session:
        data = requests.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%s&format=json"
        % (d['steam'].strip(), session['steamID']))
        return data.text
    return "NULL"

@app.route("/")
@cross_origin()
def home():
    if 'steamID' in session:
        #return '>%s<' % d['steam']#.strip()
        #return "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%s&format=json" % (d['steam'], session['ID']), 200
        return 'Logged in as: {}'.format(json.loads(getInfo())['response']['players'][0]['personaname']), 200
    return 'Not logged in', 200

@app.route('/login')
@openID.loginhandler
def login():
    return openID.try_login('http://steamcommunity.com/openid')

@openID.after_login
def after_login(resp):
    #app.config.update(SECRET_KEY =  resp.identity_url.split('/')[-1]) <-- plz dont remove, may com in handy later
    #app.secret_key = resp.identity_url.split('/')[-1]
    session['steamID'] =  resp.identity_url.split('/')[-1]
    #user =  resp.identity_url.split('/')[-1]
    #user = app.config['SECRET_KEY']
    resp = make_response(redirect(openID.get_next_url()))
    #resp.set_cookie('name', 'F. Uck', max_age=60*60)
    return resp

@app.route("/logout")
def logout():
    session.pop('steamID', None)
    return redirect(url_for('home'))
