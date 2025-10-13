from django.urls import path
from . import views

urlpatterns = [
    path('seasons/', views.seasons, name='seasons'),
    path('seasons/<int:season>', views.races, name='races'),
    path('races/', views.all_races, name='all-races'),
    path('races/<slug:slug>', views.race_detail, name='race-detail'),
    path('upload/', views.upload_race, name='upload')
]
