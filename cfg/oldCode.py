@app.route('/steam', methods=['GET'])
def steam():
    steam_openid_url = 'https://steamcommunity.com/openid/login'
    params = {
        'openid.ns': "http://specs.openid.net/auth/2.0",
        'openid.identity': "http://specs.openid.net/auth/2.0/identifier_select",
        'openid.claimed_id': "http://specs.openid.net/auth/2.0/identifier_select",
        'openid.mode': 'checkid_setup',
        'openid.return_to': 'http://127.0.0.1:5000/account-setup',  # put your url where you want to be redirect
        'openid.realm': 'http://127.0.0.1:5000/account-setup'  # not sure what it is
    }
    param_string = parse.urlencode(params)
    auth_url = steam_openid_url + "?" + param_string
    return redirect(auth_url)

@app.route('/account-setup', methods=['GET', 'POST'])
def create_or_login():
    steam_id_re = re.compile('steamcommunity.com/openid/id/(.*?)$')
    match = steam_id_re.search(dict(request.args)['openid.identity'][0])
    steamid = match.group(1)
    steam_data = get_steam_user_info(steamid)
    #print(steam_data)
    return redirect('http://localhost:4200/steam-auth;steamid=' + steam_data['steamid'])

def get_steam_user_info(steam_id):
    key = {
        'key': d['steam'].strip(),
        'steamids': steam_id # from who you want to get the information. if you are giving a array, you need to change some code here.
    }
    url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0001/?%s' \
          % parse.urlencode(key)
    rv = requests.get(url).json()
    avatar = rv['response']['players']['player'][0]['avatar']
    return rv['response']['players']['player'][0] or {}

@app.route('/avatar', methods=['GET'])
@cross_origin()
def get_avatar():
    print("jemoeder")
    try:
        id = request.args['steamid']
        print(id)
        url = {"url": "/fe/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb.jpg"}
        return jsonify(url)
        # avatar_dict = {"url": get_steam_user_info(id)['avatar']}
        # return jsonify(avatar_dict)
    except KeyError:
        print("oeps")
        return jsonify({"url": "fake news"})
