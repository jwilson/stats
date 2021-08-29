from unicodedata import category
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, DetailView
from django.db.models import Count

from .models import Team


class HomeView(TemplateView):
    template_name = 'core/home.html'


class TeamsListView(ListView):
    model = Team


class TeamStatsView(DetailView):
    model = Team
