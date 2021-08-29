import pytz

from django.test import TestCase
from django.conf import settings
from django.utils import timezone

from core.models import Season, Team


class SeasonTestCase(TestCase):
    def test_season_displays_proper_years(self):
        tz = pytz.timezone(settings.TIME_ZONE)
        s1_start_date = tz.localize(timezone.datetime.strptime('2021-09-27', '%Y-%m-%d'))
        s1_end_date = tz.localize(timezone.datetime.strptime('2022-01-15', '%Y-%m-%d'))
        s2_start_date = tz.localize(timezone.datetime.strptime('2020-03-16', '%Y-%m-%d'))
        s2_end_date = tz.localize(timezone.datetime.strptime('2020-11-09', '%Y-%m-%d'))
        s1 = Season.objects.create(start_date=s1_start_date, end_date=s1_end_date)
        s2 = Season.objects.create(start_date=s2_start_date, end_date=s2_end_date)
        self.assertEqual("21/22", s1.__str__())
        self.assertNotEqual("2021", s1.__str__())
        self.assertEqual("2020", s2.__str__())
        self.assertNotEqual("20/20", s2.__str__())

    def test_team_logo_url(self):
        t1 = Team.objects.create(name='TEAM NAME',
                                abbreviation='TEA',
                                nfl_com_link='https://www.team.com',
                                alternate_abbreviation='MAET')
        url = 'https://static.nfl.com/static/content/public/static/wildcat/assets/img/logos/teams/{}.svg'.format('MAET')
        self.assertEqual(url, t1.logo_url)
        t2 = Team.objects.create(name='TEAM2 NAME',
                                abbreviation='TEA2',
                                nfl_com_link='https://www.team2.com')
        url = 'https://static.nfl.com/static/content/public/static/wildcat/assets/img/logos/teams/{}.svg'.format('2MAET')
        self.assertNotEqual(url, t2.logo_url)
        url = 'https://static.nfl.com/static/content/public/static/wildcat/assets/img/logos/teams/{}.svg'.format('TEA2')
        self.assertEqual(url, t2.logo_url)