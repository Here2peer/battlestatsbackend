from flask import Flask, session, request, redirect, url_for, g
from flask_openid import OpenID
import json
import players
import matches

app = Flask(__name__)
app.config.update(
    SECRET_KEY = 'ApiKey.txt',
    DEBUG = True
)
openID = OpenID(app)

@app.route("/")
def home():
    return matches.getMatchesJson(), 200

def getInfo():
    request.get("http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key=%s&steamids=%d" % (SECRET_KEY, g.user))
    data = json.loads(request.data)
    return data['response'] or {}

@app.route('/login')
@openID.loginhandler
def login():
    return openID.try_login('http://steamcommunity.com/openid')

@openID.after_login
def go(resp):
    g.user = resp.identity_url
    return redirect(url_for('home'))

@app.route("/logout")
def logout():
    session.pop('openid', None)
    return redirect(url_for('home'))
