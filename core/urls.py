from django.urls import path, include


from . import views


app_name = 'core'

urlpatterns = [
    # path('weapons/create', views.WeaponCreateView.as_view(), name='weapon-create-view'),
    # path('weapons', views.WeaponsView.as_view(), name='weapons-view'),
    path('players/<int:pk>/', views.PlayerView.as_view(), name='player-stats-view'),
    path('players/', views.PlayersListView.as_view(), name='players-view'),
    path('teams/<int:pk>/', views.TeamStatsView.as_view(), name='team-stats-view'),
    path('teams/', views.TeamsListView.as_view(), name='teams-view'),
    path('', views.HomeView.as_view(), name='home-view'),
]