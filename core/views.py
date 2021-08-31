from unicodedata import category
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from django.db.models import Count

from .models import Team, Player, PlayerSeasonStats, Season


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['current_season'] = Season.get_current_season()
        return ctx


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
        qs = qs.filter(season__current=True).order_by('player__name')
        return qs


class PlayerView(DetailView):
    model = Player
    template_name = 'core/player_details.html'
