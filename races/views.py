from .models import Season, Race, Runner, Result
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UploadRaceForm
from .utils import handle_race_file

import logging
logger = logging.getLogger(__name__)


def seasons(request):
    seasons = Season.objects.all()

    context = {
        'seasons': seasons
    }
    return render(request, 'seasons.html', context)


def races(request, season):
    season = get_object_or_404(Season, season=season)
    races = Race.objects.filter(season=season)

    if request.method == "POST":
        form = UploadRaceForm(request.POST, request.FILES)
        if form.is_valid():
            # In order to handle the Excel file with race data, the function needs to know the season
            handle_race_file(form.cleaned_data["excel_file"], season)
            return redirect('races', season=season.season)
        else:
            logger.debug(f"Form validation failed: {form.errors}")
    else:
        form = UploadRaceForm()

    context = {
        'races': races,
        'season': season,
        'form': form
    }

    return render(request, 'races.html', context)


def all_races(request):
    races = Race.objects.all()

    context = {
        'races': races
    }

    return render(request, 'all_races.html', context)


def race_detail(request, slug):
    race = get_object_or_404(Race, slug=slug)
    results = Result.objects.filter(race_id=race.id).order_by('time')

    context = {
        'race': race,
        'results': results
    }

    return render(request, 'race_detail.html', context)
