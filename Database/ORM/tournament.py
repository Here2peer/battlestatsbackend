from mongoengine import *


class Team(Document):
    id = StringField(max_length=50)
    name = StringField(max_length=50)
    player1 = StringField(max_length=50)
    player2 = StringField(max_length=50)
    player3 = StringField(max_length=50)


class Match(Document):
    team1 = ReferenceField(Team)
    team2 = ReferenceField(Team)
    winner = ReferenceField(Team)


class ProposedMatch(Document):
    team1 = ReferenceField(Team)
    team2 = ReferenceField(Team)
    winner = ReferenceField(Team)


class Tournament(Document):
    tournamentID = IntField()
    participating_teams = ListField(ReferenceField(Team))
    played_matches = ListField(ReferenceField(Match))
    matches_next_round = ListField(ReferenceField(ProposedMatch))
    status = StringField(max_length=50)


def createTournament(id, team_id, tstatus):
    Tournament(
        tournamentID=id,
        teamID=team_id,
        status=tstatus
    ).save()


def getTournament(id):
    for tournament in Tournament.objects(tournamentID=id):
        return tournament
