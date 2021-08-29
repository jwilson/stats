from django.contrib import admin

from core.models import Player, Team, PlayerSeasonStats, Season


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['start_date', 'end_date', 'current']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'position']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(PlayerSeasonStats)
class PlayerSeasonStats(admin.ModelAdmin):
    list_display = ['player', 'team', 'season']

