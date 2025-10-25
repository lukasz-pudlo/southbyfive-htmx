from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.all_races, name='all-races'),
    path('seasons/', views.seasons, name='seasons'),
    path('seasons/<int:season>', views.races, name='races'),
    path('races/', views.all_races, name='all-races'),
    path('races/<slug:slug>', views.race_detail, name='race-detail'),
    path('classification/<slug:slug>', views.classification_detail,
         name='classification-detail'),
    path('favicon.ico', RedirectView.as_view(
        url='/static/favicon.ico', permanent=True))
]
