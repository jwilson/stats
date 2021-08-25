from django.contrib import admin

from core.models import Weapon, Armor#, Element, Character, Spell, Item, Enemy, \
    #State


@admin.register(Weapon)
class WeaponAdmin(admin.ModelAdmin):
    list_display = ['name', 'kind']


# @admin.register(Element)
# class ElementAdmin(admin.ModelAdmin):
#     list_display = ['name']


@admin.register(Armor)
class ArmorAdmin(admin.ModelAdmin):
    list_display = ['name', 'kind']


# @admin.register(Character)
# class CharacterAdmin(admin.ModelAdmin):
#     list_display = ['name']


# @admin.register(Spell)
# class SpellAdmin(admin.ModelAdmin):
#     list_display = ['name', 'min_level']


# @admin.register(Item)
# class ItemAdmin(admin.ModelAdmin):
#     list_display = ['name', 'min_level']


# @admin.register(Enemy)
# class EnemyAdmin(admin.ModelAdmin):
#     list_display = ['name']


# @admin.register(State)
# class StateAdmin(admin.ModelAdmin):
#     list_display = ['name']
