from django import forms

from core.models import Weapon, Armor #, Element, Spell, State, Item, Character, Enemy


class WeaponCreateForm(forms.ModelForm):
    class Meta:
        model = Weapon
        fields = ['name', 'kind', 'image', 'level', 'health', 'energy', 
            'stamina', 'intellect', 'endurance', 'resistance', 
            'red_resistance', 'blue_resistance', 'green_resistance',
            'white_resistance', 'black_resistance', 'damage', 'red_damage',
            'blue_damage', 'green_damage', 'white_damage', 'black_damage', 
            'durability', 'weight', 'description']
        


# class ElementCreateForm(forms.ModelForm):
#     class Meta:
#         model = Element
#         fields = ['name', 'icon']


class ArmorCreateForm(forms.ModelForm):
    class Meta:
        model = Armor
        fields = ['name', 'kind', 'image', 'level', 'health', 'energy', 
            'stamina', 'intellect', 'endurance', 'resistance', 
            'red_resistance', 'blue_resistance', 'green_resistance',
            'white_resistance', 'black_resistance', 'damage', 'red_damage',
            'blue_damage', 'green_damage', 'white_damage', 'black_damage', 
            'durability', 'weight', 'description']


# class SpellCreateForm(forms.ModelForm):
#     class Meta:
#         model = Armour
#         fields = ['name', 'icon', 'min_level']


# class StateCreateForm(forms.ModelForm):
#     class Meta:
#         model = State
#         fields = ['name']


# class CharacterCreateForm(forms.ModelForm):
#     class Meta:
#         model = Character
#         fields = ['name']


# class EnemyCreateForm(forms.ModelForm):
#     class Meta:
#         model = Enemy
#         fields = ['name']


# class ItemCreateForm(forms.ModelForm):
#     class Meta:
#         model = Item
#         fields = ['name', 'icon', 'min_level']
