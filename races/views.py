from django.shortcuts import get_object_or_404, render

from .models import Season, Race, Runner, Result


def seasons(request):
    seasons = Season.objects.all()

    context = {
        'seasons': seasons
    }
    return render(request, 'seasons.html', context)


def races(request, season):
    season = get_object_or_404(Season, season=season)
    races = Race.objects.filter(season=season)

    context = {
        'races': races
    }
    return render(request, 'races.html', context)


def race_detail(request, slug):
    race = get_object_or_404(Race, slug=slug)

    context = {
        'race': race
    }

    return render(request, 'race_detail.html', context)
