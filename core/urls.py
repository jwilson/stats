from django.urls import path, include


from . import views


app_name = 'core'

urlpatterns = [
    # path('elements', views.ElementsView.as_view(), name='elements-view'),
    # path('states', views.StatesView.as_view(), name='states-view'),
    # path('enemies', views.EnemiesView.as_view(), name='enemies-view'),
    # path('items', views.ItemsView.as_view(), name='items-view'),
    # path('locations', views.LocationsView.as_view(), name='locations-view'),
    # path('characters', views.CharactersView.as_view(), name='characters-view'),
    path('armors/create', views.ArmorCreateView.as_view(), name='armor-create-view'),
    path('armors', views.ArmorsView.as_view(), name='armors-view'),
    path('weapons/create', views.WeaponCreateView.as_view(), name='weapon-create-view'),
    path('weapons', views.WeaponsView.as_view(), name='weapons-view'),
    # path('spells', views.SpellsView.as_view(), name='spells-view'),
    # path('abilities', views.AbilitiesView.as_view(), name='abilities-view'),
    # path('quests', views.QuestsView.as_view(), name='quests-view'),
    # path('test', views.TestView.as_view(), name='test-view'),
    path('', views.HomeView.as_view(), name='home-view'),
]