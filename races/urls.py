from django.urls import path
from . import views

urlpatterns = [
    path('', views.seasons, name='seasons'),
    path('<int:season>/races', views.races, name='races'),
]
