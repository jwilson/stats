from django.db import models
from django.conf import settings
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


POSITIONS = (
    ('RB', _("Runningback")),
    ('QB', _("Quarterback")),
    ('WR', _("Wide Receiver")),
    ('FB', _("Fullback")),
    ('P', _("Punter")),
    ('TE', _("Tightend")),
    ('NT', _("Nose Tackle")),
    ('DB', _("Defensiveback")),
    ('SS', _("Strong Safety")),
    ('K', _("Kicker"))
)


CONFERENCES = (
    ('AFC', _("AFC")),
    ('NFC', _("NFC"))
)

DIVISIONS = (
    ('N', _("North")),
    ('S', _("South")),
    ('E', _("East")),
    ('W', _("West"))
)


class STATS_CACHE_MIXIN(object):
    def get_cached_stat(self, key, q, timeout, order_by=None):
        stats = cache.get(key)
        if not stats:
            stats = self.season_stats.filter(q)
            if order_by:
                stats = stats.order_by(order_by)
            cache.set(key, stats, timeout=timeout)
        return stats


class Franchise(models.Model):
    name = models.CharField(max_length=255, help_text="The name of the overall organization")


class Season(models.Model):
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    current = models.BooleanField(default=False)

    def __str__(self):
        if self.start_date.year == self.end_date.year:
            return '{}'.format(self.start_date.year)
        return '{}/{}'.format(self.start_date.strftime('%y'), self.end_date.strftime('%y'))

    @classmethod
    def get_current_season(cls):
        return Season.objects.get(current=True)


class Player(STATS_CACHE_MIXIN, models.Model):
    name = models.CharField(max_length=255, help_text="The full name of the player.")
    position = models.CharField(max_length=255, choices=POSITIONS, help_text="The player's position")

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return '{} - {}'.format(self.name, self.position)

    def get_current_season_stats(self):
        key = 'current-season-player-stats-{}'.format(self.id)
        if not hasattr(self, '_current_season_stats'):
            q = Q(season__current=True)
            self._current_season_stats = self.get_cached_stat(key, q, settings.PLAYER_STATS_TIMEOUT)
        return self._current_season_stats

    def get_previous_seasons_stats(self):
        key = 'previous-season-player-stats-{}'.format(self.id)
        if not hasattr(self, '_previous_season_stats'):
            q = Q(season__current=False)
            order_by = 'season__start_date'
            self._previous_season_stats = self.get_cached_stat(key, q, settings.PLAYER_STATS_TIMEOUT, order_by=order_by)
        return self._previous_season_stats


class Team(STATS_CACHE_MIXIN, models.Model):
    name = models.CharField(max_length=255, help_text="The long form team name (ex. Seattle Seahawks)")
    abbreviation = models.CharField(max_length=255, help_text="The abbreviation of the team (ex. SEA)")
    nfl_com_link = models.CharField(max_length=255, help_text="The nfl.com team website address.")
    alternate_abbreviation = models.CharField(max_length=255, help_text="The alternate/newer  abbreviation of the team (ex. LAC)")
    conference = models.CharField(max_length=255, choices=CONFERENCES, help_text="The division the team is currently in.")
    division = models.CharField(max_length=255, choices=DIVISIONS, help_text="The division the team is currently in.")

    def __str__(self):
        return '{} ({})'.format(self.name, self.abbreviation)

    @property
    def logo_url(self):
        abbr = self.alternate_abbreviation or self.abbreviation
        url = 'https://static.www.nfl.com/league/api/clubs/logos/{}.svg'.format(abbr)
        return url

    def get_current_season_stats(self):
        key = 'current-season-team-stats-{}'.format(self.id)
        if not hasattr(self, '_current_season_stats'):
            q = Q(season__current=True)
            self._current_season_stats = self.get_cached_stat(key, q, settings.TEAM_STATS_TIMEOUT)
        return self._current_season_stats

    def _get_season_stats_ordered(self, filter):
        return self.get_current_season_stats().order_by(filter)

    def get_current_season_rushing_attempts_leader(self):
        return self._get_season_stats_ordered('-attempts').first()

    def get_current_season_rushing_yards_leader(self):
        return self._get_season_stats_ordered('-yards').first()

    def get_current_season_rushing_touchdowns_leader(self):
        return self._get_season_stats_ordered('-touchdowns').first()

    def get_current_season_rushing_1st_leader(self):
        return self._get_season_stats_ordered('-first_down').first()

    def _get_total_rushing_stats(self):
        key = 'rushing-yards-{}{}{}'.format(self.conference, self.division, self.abbreviation)
        current_stats = cache.get(key)
        if not current_stats:
            # current_season = Season.get_current_season()
            # current_stats = PlayerSeasonStats.objects.filter(team=self, season=current_season)
            # post coding session
            current_stats = self.season_stats.filter(season__current=True)
            cache.set(key, current_stats, timeout=settings.TEAM_STATS_TIMEOUT)
        return current_stats

    def get_total_rushing_stats(self):
        current_stats = self._get_total_rushing_stats()
        return sum([stat.yards for stat in current_stats])

    def test(self):
        cs = self._get_total_rushing_stats()
        lc = [stat.yards for stat in current_stats]
        return self.calc(len(cs), lc)

    def calc(self, l, lc):
        total = sum(lc)
        return total / l

    def get_average_rushing_stats(self):
        current_stats = self._get_total_rushing_stats()
        total = sum([stat.yards for stat in current_stats])
        num = len(current_stats)
        return total / num

    def get_avg_avg_stats(self):
        current_stats = self._get_total_rushing_stats()
        total = sum([stat.average for stat in current_stats])
        num = len(current_stats)
        return total / num
        
    @classmethod
    def get_conference_division_teams(cls, conference_teams, division):
        conference = ''
        if conference_teams:
            conference = conference_teams.first().conference
        key = 'divison-teams-{}{}'.format(conference, division)
        division_teams = cache.get(key)
        if not division_teams:
            division_teams = conference_teams.filter(division=division)
            cache.set(key, division_teams, timeout=settings.TEAM_STATS_TIMEOUT)
        return division_teams

    @classmethod
    def get_conference_teams(cls, conference):
        key = 'conference-teams-{}'.format(conference)
        conference_stats = cache.get(key)
        if not conference_stats:
            conference_stats = cls.objects.filter(conference=conference)
            cache.set(key, conference_stats, timeout=settings.TEAM_STATS_TIMEOUT)
        return conference_stats


class PlayerSeasonStats(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='season_stats')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='season_stats')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='season_stats')
    attempts = models.PositiveIntegerField(default=0)
    attempts_game = models.FloatField(default=0)
    yards = models.IntegerField(default=0)
    average = models.FloatField(default=0)
    yards_game = models.FloatField(default=0)
    touchdowns = models.PositiveIntegerField(default=0)
    longest_gains = models.IntegerField(default=0)
    longest_gains_touchdown = models.BooleanField(default=False)
    first_down = models.PositiveIntegerField(default=0)
    first_down_conversion = models.FloatField(default=0)
    twenty_plus = models.PositiveIntegerField(default=0)
    forty_plus = models.PositiveIntegerField(default=0)
    fumbles = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('player__position', 'player__name')
