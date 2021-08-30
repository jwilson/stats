from unicodedata import category
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from django.db.models import Count

from .models import Team, Player, PlayerSeasonStats, Season


class HomeView(TemplateView):
    template_name = 'core/home.html'


class TeamsListView(ListView):
    model = Team


class TeamStatsView(DetailView):
    model = Team


class PlayersListView(ListView):
    model = PlayerSeasonStats
    template_name = 'core/player_list.html'
    paginate_by = 50

    def get_queryset(self):
        qs = super().get_queryset()
        current_season = Season.objects.get(current=True)
        qs = qs.filter(season=current_season).order_by('player__name')
        return qs


class PlayerStatsView(DetailView):
    model = PlayerSeasonStats
    template_name = 'core/player_details.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        current_season = Season.get_current_season()
        ctx['previous_season_stats'] = PlayerSeasonStats.objects.exclude(season=current_season)
        return ctx
