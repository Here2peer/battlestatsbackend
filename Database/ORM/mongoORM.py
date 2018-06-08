from mongoengine import *


class Champion(Document):
    name = StringField(max_length=50)
    type = StringField(max_length=50)