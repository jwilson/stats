import pytz

from django.test import TestCase
from django.conf import settings
from django.utils import timezone

from core.models import PlayerSeasonStats, Season, Team, Player


class SeasonTestCase(TestCase):
    # def test_season_displays_proper_years(self):
    #     tz = pytz.timezone(settings.TIME_ZONE)
    #     s1_start_date = tz.localize(timezone.datetime.strptime('2021-09-27', '%Y-%m-%d'))
    #     s1_end_date = tz.localize(timezone.datetime.strptime('2022-01-15', '%Y-%m-%d'))
    #     s2_start_date = tz.localize(timezone.datetime.strptime('2020-03-16', '%Y-%m-%d'))
    #     s2_end_date = tz.localize(timezone.datetime.strptime('2020-11-09', '%Y-%m-%d'))
    #     s1 = Season.objects.create(start_date=s1_start_date, end_date=s1_end_date)
    #     s2 = Season.objects.create(start_date=s2_start_date, end_date=s2_end_date)
    #     self.assertEqual("21/22", s1.__str__())
    #     self.assertNotEqual("2021", s1.__str__())
    #     self.assertEqual("2020", s2.__str__())
    #     self.assertNotEqual("20/20", s2.__str__())

    # def test_team_logo_url(self):
    #     t1 = Team.objects.create(name='TEAM NAME',
    #                             abbreviation='TEA',
    #                             nfl_com_link='https://www.team.com',
    #                             alternate_abbreviation='MAET')
    #     url = 'https://static.nfl.com/static/content/public/static/wildcat/assets/img/logos/teams/{}.svg'.format('MAET')
    #     self.assertEqual(url, t1.logo_url)
    #     t2 = Team.objects.create(name='TEAM2 NAME',
    #                             abbreviation='TEA2',
    #                             nfl_com_link='https://www.team2.com')
    #     url = 'https://static.nfl.com/static/content/public/static/wildcat/assets/img/logos/teams/{}.svg'.format('2MAET')
    #     self.assertNotEqual(url, t2.logo_url)
    #     url = 'https://static.nfl.com/static/content/public/static/wildcat/assets/img/logos/teams/{}.svg'.format('TEA2')
    #     self.assertEqual(url, t2.logo_url)

    def test_team_rushing_stats(self):
        tz = pytz.timezone(settings.TIME_ZONE)
        s1_start_date = tz.localize(timezone.datetime.strptime('2021-09-27', '%Y-%m-%d'))
        s1_end_date = tz.localize(timezone.datetime.strptime('2022-01-15', '%Y-%m-%d'))
        s1 = Season.objects.create(start_date=s1_start_date, end_date=s1_end_date, current=True)
        t1 = Team.objects.create(name="TEST1", abbreviation="TEA", nfl_com_link='', alternate_abbreviation='TEA')
        p1 = Player.objects.create(name='TESTP1', position='QB')
        p2 = Player.objects.create(name='TESTP1', position='RB')
        PlayerSeasonStats.objects.create(
            player=p1,
            season=s1,
            team=t1,
            yards=3,
            first_down_conversion=4,

        )
        PlayerSeasonStats.objects.create(
            player=p1,
            season=s1,
            team=t1,
            yards=13,
            first_down_conversion=5,
        )
        rushing_stats = t1.get_total_rushing_stats()
        self.assertEqual(rushing_stats, 16)
        # post coding session
        PlayerSeasonStats.objects.create(
            player=p1,
            season=s1,
            team=t1,
            yards=1,
            first_down_conversion=5,
        )
        rushing_stats = t1.get_total_rushing_stats()
        self.assertNotEqual(rushing_stats, 16)
        self.assertEqual(rushing_stats, 17)
    
    def test_team_average_rushing_stats(self):
        tz = pytz.timezone(settings.TIME_ZONE)
        s1_start_date = tz.localize(timezone.datetime.strptime('2021-09-27', '%Y-%m-%d'))
        s1_end_date = tz.localize(timezone.datetime.strptime('2022-01-15', '%Y-%m-%d'))
        s1 = Season.objects.create(start_date=s1_start_date, end_date=s1_end_date, current=True)
        t1 = Team.objects.create(name="TEST1", abbreviation="TEA", nfl_com_link='', alternate_abbreviation='TEA')
        p1 = Player.objects.create(name='TESTP1', position='QB')
        p2 = Player.objects.create(name='TESTP1', position='RB')
        PlayerSeasonStats.objects.create(
            player=p1,
            season=s1,
            team=t1,
            average=4,
            first_down_conversion=14,

        )
        PlayerSeasonStats.objects.create(
            player=p1,
            season=s1,
            team=t1,
            average=6,
            first_down_conversion=15,
        )
        
        avg_avg_stats = t1.get_avg_avg_stats()
        
        self.assertEqual(avg_avg_stats, 5.0)
        # post coding session
        PlayerSeasonStats.objects.create(
            player=p1,
            season=s1,
            team=t1,
            average=8,
            first_down_conversion=15,
        )
        avg_avg_stats = t1.get_avg_avg_stats()
        self.assertNotEqual(avg_avg_stats, 5.0)
        self.assertEqual(avg_avg_stats, 6.0)
