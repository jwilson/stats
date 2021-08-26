import json

from django.core.management.base import BaseCommand
from django.conf import settings

from core.models import Player, Team

class Command(BaseCommand):
    def handle(self, *args, **options):
        filename = '{}/stats.json'.format(settings.BASE_DIR)
        rushing_json_data = open(filename, 'r').read()
        rushing_data = json.loads(rushing_json_data)
        teams = {}
        players = []
        for player_stat in rushing_data:
            team_name = player_stat['Team']
            if team_name not in teams:
                team, _ = Team.objects.get_or_create(name=team_name,
                                                     abbreviation=team_name)
                teams[team_name] = team
            longgains = player_stat['Lng']
            longgains_team = False
            if longgains[-1:] == 'T':
                longgains_team = True
                longgains = longgains[:-1]
            player = Player(name=player_stat['Player'],
                            position=player_stat['Pos'])
            player.team_name = player_stat['Team']
            players.append(player)

            """
            attempts=player_stat['Att'],
                            attempts_game=player_stat['Att/G'],
                            yards=player_stat['Yds'],
                            average=player_stat['Avg'],
                            yards_game=player_stat['Yds/G'],
                            touchdowns=player_stat['TD'],
                            longgains=int(longgains),
                            longgains_team=longgains_team,
                            first_down=player_stat['1st'],
                            first_down_conversion=player_stat['1st%'],
                            twenty_plus=player_stat['20+'],
                            forty_plus=player_stat['40+'],
                            fumbles=player_stat['FUM']
            """
        added_players = Player.objects.bulk_create(players)
        for player in added_players:
            team = teams[player.team_name]
            player.team.set(team)


