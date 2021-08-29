import json
import locale

from dateutil.relativedelta import relativedelta

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

from core.models import Player, Team, Season, PlayerSeasonStats, Franchise

TEAMS = {
    'OAK': {'n': 'Oakland Raiders', 'a': 'LV', 'c': 'AFC', 'd': 'W'},
    'WAS': {'n': 'Washington FBT', 'a': 'WAS', 'c': 'NFC', 'd': 'E'},
    'CIN': {'n': 'Cincinnati Bengals', 'a': 'CIN', 'c': 'AFC', 'd': 'N'},
    'SD': {'n': 'San Diego Chargers', 'a': 'LAC', 'c': 'AFC', 'd': 'W'},
    'CAR': {'n': 'Carolina Panthers', 'a': 'CAR', 'c': 'NFC', 'd': 'S'},
    'GB': {'n': 'Green Bay Packers', 'a': 'GB', 'c': 'NFC', 'd': 'N'},
    'NYG': {'n': 'New York Giants', 'a': 'NYG', 'c': 'NFC', 'd': 'E'},
    'DET': {'n': 'Detroit Lions', 'a': 'DET', 'c': 'NFC', 'd': 'N'},
    'LA': {'n': 'Los Angeles Rams', 'a': 'LA', 'c': 'NFC', 'd': 'W'},
    'IND': {'n': 'Indianapolis Colts', 'a': 'IND', 'c': 'AFC', 'd': 'S'},
    'JAX': {'n': 'Jacksonville Jaguars', 'a': 'JAX', 'c': 'AFC', 'd': 'S'},
    'BUF': {'n': 'Buffalo Bills', 'a': 'BUF', 'c': 'AFC', 'd': 'E'},
    'CLE': {'n': 'Cleveland Browns', 'a': 'CLE', 'c': 'AFC', 'd': 'N'},
    'NYJ': {'n': 'New York Jets', 'a': 'NYJ', 'c': 'AFC', 'd': 'E'},
    'NE': {'n': 'New England Patriots', 'a': 'NE', 'c': 'AFC', 'd': 'E'},
    'MIA': {'n': 'Miami Dolphins', 'a': 'MIA', 'c': 'AFC', 'd': 'E'},
    'SF': {'n': 'San Fransico 49ers', 'a': 'SF', 'c': 'NFC', 'd': 'W'},
    'DEN': {'n': 'Denver Broncos', 'a': 'DEN', 'c': 'AFC', 'd': 'W'},
    'NO': {'n': 'New Orleans Saints', 'a': 'NO', 'c': 'NFC', 'd': 'S'},
    'DAL': {'n': 'Dallas Cowboys', 'a': 'DAL', 'c': 'NFC', 'd': 'E'},
    'MIN': {'n': 'Minnesota Vikings', 'a': 'MIN', 'c': 'NFC', 'd': 'N'},
    'TEN': {'n': 'Tennesse Titans', 'a': 'TEN', 'c': 'AFC', 'd': 'S'},
    'ARI': {'n': 'Arizona Cardinals', 'a': 'ARI', 'c': 'NFC', 'd': 'W'},
    'BAL': {'n': 'Baltimore Ravens', 'a': 'BAL', 'c': 'AFC', 'd': 'N'},
    'TB': {'n': 'Tamba Bay Bucaneers', 'a': 'TB', 'c': 'NFC', 'd': 'S'},
    'HOU': {'n': 'Houston Texans', 'a': 'HOU', 'c': 'AFC', 'd': 'S'},
    'PIT': {'n': 'Pittsburgh Steelers', 'a': 'PIT', 'c': 'AFC', 'd': 'N'},
    'CHI': {'n': 'Chicago Bears', 'a': 'CHI', 'c': 'NFC', 'd': 'N'},
    'SEA': {'n': 'Seattle Seahawks', 'a': 'SEA', 'c': 'NFC', 'd': 'W'},
    'ATL': {'n': 'Atlanta Falcons', 'a': 'ATL', 'c': 'NFC', 'd': 'S'},
    'KC': {'n': 'Kansas City Chiefs', 'a': 'KC', 'c': 'AFC', 'd': 'W'},
    'PHI': {'n': 'Philadelphia Eagles', 'a': 'PHI', 'c': 'NFC', 'd': 'E'}
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8' )
        now = timezone.now()
        filename = '{}/stats.json'.format(settings.BASE_DIR)
        rushing_json_data = open(filename, 'r').read()
        rushing_data = json.loads(rushing_json_data)
        season = Season.objects.create(start_date=now-relativedelta(weeks=16),
                                       end_date=now)
        teams = {}
        teams_to_bulk_create = []
        # franchises_to_bulk_create = []
        players_to_bulk_create = []
        stats_to_bulk_create = []

        added = 0

        for stat in rushing_data:
            team_name = stat['Team']
            if team_name not in teams:
                added += 1
                # franchise = Franchise(name=team_name)
                # franchises_to_bulk_create.append(franchise)
                team_data = TEAMS[team_name]
                team = Team(name=team_data['n'],
                            abbreviation=team_name,
                            alternate_abbreviation=team_data['a'],
                            conference=team_data['c'],
                            division=team_data['d'])  # , franchise_id=added)
                teams_to_bulk_create.append(team)
                teams[team_name] = team
            player = Player(name=stat['Player'], position=stat['Pos'])
            players_to_bulk_create.append(player)

        # Franchise.objects.bulk_create(franchises_to_bulk_create)
        teams = Team.objects.bulk_create(teams_to_bulk_create)
        teams_by_abbr = {team.abbreviation: team for team in teams}
        players = Player.objects.bulk_create(players_to_bulk_create)
        players_by_name = {player.name: player for player in players}

        for player_stat in rushing_data:
            team = teams_by_abbr[player_stat['Team']]
            player = players_by_name[player_stat['Player']]

            longgains = player_stat['Lng']
            longgains_team = False
            try:
                int(longgains)
            except ValueError:
                longgains_team = True
                longgains = longgains[:-1]

            yards = player_stat['Yds']
            try:
                int(yards)
            except ValueError:
                yards = locale.atoi(yards)

            stat = PlayerSeasonStats(player=player,
                                     team=team,
                                     season=season,
                                     attempts=player_stat['Att'],
                                     attempts_game=player_stat['Att/G'],
                                     yards=yards,
                                     average=player_stat['Avg'],
                                     yards_game=player_stat['Yds/G'],
                                     touchdowns=player_stat['TD'],
                                     longgains=int(longgains),
                                     longgains_team=longgains_team,
                                     first_down=player_stat['1st'],
                                     first_down_conversion=player_stat['1st%'],
                                     twenty_plus=player_stat['20+'],
                                     forty_plus=player_stat['40+'],
                                     fumbles=player_stat['FUM'])
            stats_to_bulk_create.append(stat)
        
        PlayerSeasonStats.objects.bulk_create(stats_to_bulk_create)

