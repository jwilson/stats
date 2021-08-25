from unicodedata import category
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from django.db.models import Count

from core.models import Weapon, Armor
from core.forms import WeaponCreateForm, ArmorCreateForm#, CharacterCreateForm, \
    #ItemCreateForm, EnemyCreateForm, SpellCreateForm, ElementCreateForm, \
    #StateCreateForm


class HomeView(TemplateView):
    template_name = 'core/base.html'


# class TestView(TemplateView):
#     template_name = 'core/list_base.html'


# class QuestsView(TemplateView):
#     template_name = 'core/quests/quests_base.html'


# class AbilitiesView(TemplateView):
#     template_name = 'core/abilities/abilities_base.html'


# class SpellsView(TemplateView):
#     template_name = 'core/spells/spells_base.html'
#     form_class = SpellCreateForm


class WeaponsView(ListView):
    template_name = 'core/weapons/weapons_base.html'
    model = Weapon
    paginate_by = 25


class WeaponCreateView(CreateView):
    template_name = 'core/weapons/weapon_create.html'
    form_class = WeaponCreateForm
    model = Weapon


class ArmorsView(TemplateView):
    template_name = 'core/armors/armors_base.html'
    form_class = ArmorCreateForm


class ArmorCreateView(CreateView):
    template_name = 'core/armors/armors_create.html'
    form_class = ArmorCreateForm
    model = Armor


# class CharactersView(TemplateView):
#     template_name = 'core/characters/characters_base.html'
#     form_class = CharacterCreateForm


# class LocationsView(TemplateView):
#     template_name = 'core/locations/locations_base.html'


# class ItemsView(TemplateView):
#     template_name = 'core/items/items_base.html'
#     form_class = ItemCreateForm


# class EnemiesView(TemplateView):
#     template_name = 'core/enemies/enemies_base.html'
#     form_class = EnemyCreateForm


# class StatesView(TemplateView):
#     template_name = 'core/states/states_base.html'
#     form_class = StateCreateForm


# class ElementsView(TemplateView):
#     template_name = 'core/elements/elements_base.html'
#     form_class = ElementCreateForm
