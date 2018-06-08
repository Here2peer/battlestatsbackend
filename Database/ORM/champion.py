from mongoengine import *

class Ability(Document):
    icon = StringField(max_length=150)
    name = StringField(max_length=50)
    description = StringField(max_length=250)


class Battlerites(document):
    icon = StringField(max_length=150)
    name = StringField(max_length=50)
    abilitySlot = IntField
    description = StringField(max_length=250)


class Champion(Document):
    icon = StringField(max_length=150)
    name = StringField(max_length=50)
    description = StringField(max_length=250)
    ability = ListField(ReferenceField(Ability))
    battlerites = ListField(ReferenceField(Battlerites))


# create a new champion and save it to the database
def createChampion(cicon, cname, cdescr, abilities, cbattlerites):
    Champion(
        icon = cicon,
        name = cname,
        description = cdescr,
        ability = abilities,
        battlerites = cbattlerites
    ).save()


#retrieve a champion from the database
def getChampion(championName):
    for champion in Champion.objects(name = championName):
        return champion


def getAllChampions():
    champions = []
    for champion in Champion.objects:
        champions.append(champion)
    return champions
