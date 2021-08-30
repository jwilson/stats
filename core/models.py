from django.db import models
from django.conf import settings
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
    ('S', _("Soouth")),
    ('E', _("East")),
    ('W', _("West"))
)


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


class Player(models.Model):
    name = models.CharField(max_length=255, help_text="The full name of the player.")
    position = models.CharField(max_length=255, choices=POSITIONS, help_text="The player's position")

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return '{} - {}'.format(self.name, self.position)


class Team(models.Model):
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
        current_season = Season.objects.get(current=True)
        current_stats = self.season_stats.filter(season=current_season)
        return current_stats


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
    first_down_conversion = models.FloatField()
    twenty_plus = models.PositiveIntegerField(default=0)
    forty_plus = models.PositiveIntegerField(default=0)
    fumbles = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('player__position', 'player__name')
