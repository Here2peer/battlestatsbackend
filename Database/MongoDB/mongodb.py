from flask_mongoengine import MongoEngine


def initialise_database(app):
    mongo_port = 27017
    mongo_user = 'bsdbuser'
    mongo_pass = 'nsPzs3Fk8jIEHySD'

    app.config['MONGODB_SETTINGS'] = {
        'db': 'battlestatsdb',
        'host': 'mongodb+srv://battlestatsdb-kjoco.mongodb.net/test',
        'port': 27017,
        'username': mongo_user,
        'password': mongo_pass
    }
    db = MongoEngine(app)
    return db