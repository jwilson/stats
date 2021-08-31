import csv

from unicodedata import category
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, DetailView, View
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse 
from django.urls import reverse
from django.utils import timezone
from django.core.cache import cache

from .models import Team, Player, PlayerSeasonStats, Season
from .forms import TableSortForm


def generate_order_by(cleaned_data):
    gains = cleaned_data['longest_gains'] 
    yards = cleaned_data['yards'] 
    touchdowns = cleaned_data['touchdowns'] 
    order_by = []
    lng_sort = 'longest_gains'
    yds_sort = 'yards'
    td_sort = 'touchdowns'
    if yards == 1:
        order_by.append(yds_sort)
    elif yards == 2:
        order_by.append('-{}'.format(yds_sort))
    if touchdowns == 1:
        order_by.append(td_sort)
    elif touchdowns == 2:
        order_by.append('-{}'.format(td_sort))
    if gains == 1:
        order_by.append(lng_sort)
    elif gains == 2:
        order_by.append('-{}'.format(lng_sort))
    return order_by


class SORT_MIXIN(object):
    def sort_queryset(self, qs, form):
        if form.is_valid():
            order_by = generate_order_by(form.cleaned_data)
            qs = qs.order_by(*order_by)
        return qs

class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['current_season_stats'] = Season.get_current_season().season_stats
        self.request.session['player_filter'] = None
        return ctx


class TeamsListView(ListView):
    model = Team

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        self.request.session['player_filter'] = None
        return ctx

class TeamStatsView(SORT_MIXIN, DetailView):
    model = Team

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        current_season_stats = self.get_object().get_current_season_stats()
        form = TableSortForm(self.request.GET or None)
        ctx['lng'] = 0
        ctx['yds'] = 0
        ctx['tds'] = 0
        self.request.session['player_filter'] = None
        if form.is_valid():
            current_season_stats = self.sort_queryset(current_season_stats, form)
            cleaned_data = form.cleaned_data
            ctx['lng'] = cleaned_data['longest_gains'] 
            ctx['yds'] = cleaned_data['yards'] 
            ctx['tds'] = cleaned_data['touchdowns'] 
        ctx['current_season_stats'] = current_season_stats
        return ctx


class PlayersListView(SORT_MIXIN, ListView):
    model = PlayerSeasonStats
    template_name = 'core/player_list.html'
    paginate_by = 25

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(season__current=True).order_by('player__name')
        player_filter = self.request.session.get('player_filter', None)
        if player_filter:
            qs = qs.filter(player__name__icontains=player_filter)
        order_by = self.build_order_by()
        qs = qs.order_by(*order_by)
        return qs

    def build_order_by(self):
        form = TableSortForm(self.request.GET or None)
        order_by = []
        if form.is_valid():
            order_by = generate_order_by(form.cleaned_data)
        return order_by

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        form = TableSortForm(self.request.GET or None)
        current_season_stats = self.get_queryset()
        ctx['lng'] = 0
        ctx['yds'] = 0
        ctx['tds'] = 0
        if form.is_valid():
            cleaned_data = form.cleaned_data
            ctx['lng'] = cleaned_data['longest_gains'] 
            ctx['yds'] = cleaned_data['yards'] 
            ctx['tds'] = cleaned_data['touchdowns'] 
        return ctx


class PlayerView(DetailView):
    model = Player
    template_name = 'core/player_details.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['current_season_stats'] = self.get_object().get_current_season_stats()
        ctx['previous_season_stats'] = self.get_object().get_previous_seasons_stats()
        return ctx


class PlayerFilterView(TemplateView):
    template_name = 'core/player_list.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        player_name = self.request.GET.get('player_name', None)
        if player_name:
            self.request.session['player_filter'] = player_name
        return ctx

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('core:players-view'))


class ExportView(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(
            content_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename="export_{}.csv"'.format(timezone.now())},
        )
        writer = csv.writer(response)
        
        qs = PlayerSeasonStats.objects.filter(season__current=True).order_by('player__name')
        player_filter = self.request.session['player_filter']
        if player_filter:
            qs = qs.filter(player__name__icontains=player_filter)
            
        form = TableSortForm(self.request.GET or None)
        if form.is_valid():
            order_by = generate_order_by(form.cleaned_data)
            qs = qs.order_by(*order_by)
        
        for result in qs:
            td = '*' if result.longest_gains_touchdown else ''
            longest_gains = '{}{}'.format(result.longest_gains, td)
            writer.writerow([result.player.name,
                             result.player.position,
                             result.team.name,
                             result.attempts,
                             result.attempts_game,
                             result.yards,
                             result.average,
                             result.yards_game,
                             result.touchdowns,
                             longest_gains,
                             result.first_down,
                             result.first_down_conversion,
                             result.twenty_plus,
                             result.forty_plus,
                             result.fumbles])

        return response
