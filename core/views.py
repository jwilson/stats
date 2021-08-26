from unicodedata import category
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from django.db.models import Count


class HomeView(TemplateView):
    template_name = 'core/home.html'
