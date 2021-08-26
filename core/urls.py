from django.urls import path, include


from . import views


app_name = 'core'

urlpatterns = [
    # path('weapons/create', views.WeaponCreateView.as_view(), name='weapon-create-view'),
    # path('weapons', views.WeaponsView.as_view(), name='weapons-view'),
    path('', views.HomeView.as_view(), name='home-view'),
]