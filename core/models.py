from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from django.utils import timezone


class Team(models.Model):
    name = models.CharField(max_length=255, help_text="The long form team name (ex. Seattle Seahawks)")
    abbreviation = models.CharField(max_length=255, help_text="The abbreviation of the team (ex. SEA)")
    nfl_com_link = models.CharField(max_length=255, help_text="The nfl.com team website address.")
    logo = models.CharField(max_length=255, help_text="The wikipedia hosted logo")


POSITIONS = (
    ('RB', 'Runningback'),
    ('QB', 'Quarterback'),
    ('WR', 'Wide Receiver'),
    ('FB', 'Fullback'),
    ('P', 'Punter'),
    ('TE', 'Tightend'),
    ('NT', 'Nose Tackle'),
    ('DB', 'Defensiveback'),
    ('SS', 'Strong Safety'),
    ('K', 'Kicker')
)


class Player(models.Model):
    name = models.CharField(max_length=255, help_text="The full name of the player.")
    position = models.CharField(max_length=255, choices=POSITIONS, help_text="The player's position")
    team = models.ManyToManyField(Team, through='Stat', related_name='stats', help_text="The player's stats for a team")


class Stat(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    attempts = models.PositiveIntegerField(default=0)
    attempts_game = models.FloatField(default=0)
    yards = models.IntegerField(default=0)
    average = models.FloatField(default=0)
    yards_game = models.FloatField(default=0)
    touchdowns = models.PositiveIntegerField(default=0)
    longgains = models.PositiveIntegerField(default=0)
    longgains_team = models.BooleanField(default=False)
    first_down = models.PositiveIntegerField(default=0)
    first_down_conversion = models.FloatField()
    twenty_plus = models.PositiveIntegerField(default=0)
    forty_plus = models.PositiveIntegerField(default=0)
    fumbles = models.PositiveIntegerField(default=0)
