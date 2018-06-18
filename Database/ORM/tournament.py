from datetime import time
from mongoengine import *

class Team(Document):
    team_id = StringField(max_length=50)
    name = StringField(max_length=50)
    player1 = StringField(max_length=50)
    player2 = StringField(max_length=50)
    player3 = StringField(max_length=50)

class Match(Document):
    matchID = StringField(max_length=50)
    team1 = ReferenceField(Team)
    team2 = ReferenceField(Team)
    winner = ReferenceField(Team)

class Tournament(Document):
    tournamentID = IntField()
    lastUpdated = StringField(max_length=50)
    tournamentName = StringField(max_length=50)
    tournament_owner = StringField(max_length=50)
    num_teams = IntField()
    teams = ListField(ReferenceField(Team))
    matches = ListField(ReferenceField(Match))
    status = StringField(max_length=50)

def createTournament(owner, nteams):
    Tournament(
        tournament_owner = owner,
        lastUpdated = time(),
        num_teams = nteams,
        status="SIGNUPS"
    ).save()

def addTeam(tID, teamID, teamName, p1, p2, p3):
    for tournament in Tournament.objects(tournamentID = tID):
        if tournament.status == "SIGNUPS":
            newTeam = Team(
                team_id = teamID,
                name = teamName,
                player1 = p1,
                player2 = p2,
                player3 = p3
            ).save()
            tournament.update_one(push__teams=newTeam)
            if tournament.teams.count() == tournament.num_teams:
                tournament.status = "STARTED"
                #TODO: Start generating matches here!

def create_match(tourney_ID, team_1, team_2):
    for tournament in Tournament.objects(tournamentID = tourney_ID):
        newMatch = Match(
            team1 = team_1,
            team2 = team_2
        ).save()
        tournament.update_one(push__matches=newMatch)

def update_match(tourney_ID, match_ID, team_1, team_2, winning_team):
    for tournament in Tournament.objects(tournamentID = tourney_ID):
        for match in tournament.objects.filter((Q(team1 = team_1) and Q(team2 = team_2))):
            match(
                matchID = match_ID,

                winner = winning_team
            ).save()

def getTournament(id):
    for tournament in Tournament.objects(tournamentID=id):
        return tournament

def get_all_tournaments():
    tournaments = []
    for tournament in Tournament.objects():
        tournaments.append(tournament)
    return tournaments
