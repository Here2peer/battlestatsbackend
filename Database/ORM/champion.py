from mongoengine import *

from Database.ORM import dict_helper


class Ability(EmbeddedDocument):
    icon128 = StringField(max_length=150)
    name = StringField(max_length=50)
    description = StringField(max_length=500)


class Battlerites(EmbeddedDocument):
    icon = StringField(max_length=150)
    name = StringField(max_length=50)
    abilitySlot = IntField()
    description = StringField(max_length=500)


class Champion(Document):
    icon = StringField(max_length=150)
    name = StringField(max_length=50)
    description = StringField(max_length=500)
    ability = ListField(EmbeddedDocumentField(Ability))
    battlerites = ListField(EmbeddedDocumentField(Battlerites))
    type = StringField()


# create a new champion and save it to the database
def createChampion(cicon, cname, cdescr, abilities, cbattlerites):
    Champion(
        icon=cicon,
        name=cname,
        description=cdescr,
        ability=abilities,
        battlerites=cbattlerites
    ).save()


def create_ability(aicon, aname, adescr):
    return Ability(
        icon128=aicon,
        name=aname,
        description=adescr
    )


def create_battlerite(bicon, bname, bslot, bdescr):
    return Battlerites(
        icon=bicon,
        name=bname,
        abilitySlot=bslot,
        description=bdescr
    )


# retrieve a champion from the database
def getChampion(championName):
    for champion in Champion.objects(name=championName):
        sjempion = champion
    return sjempion


def getAllChampions():
    champions = {'characters': []}
    if Champion.objects.count() > 0:
        for champion in Champion.objects:
            champion = dict_helper.mongo_to_dict(champion, [])
            x = 1
            abilities = []
            for ability_ref in champion.pop('ability'):
                ability_string = 'ability' + str(x)
                x += 1
                champion[ability_string] = ability_ref
            champions['characters'].append(champion)
        return champions
    return 0


def clean_all_champs():
    champions = []
    if Champion.objects.count() > 0:
        for champion in Champion.objects:
            champion.delete()
            champions.append(champion)
    return champions
