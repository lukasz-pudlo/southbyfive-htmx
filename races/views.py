from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from .forms import UploadRaceForm
from .utils import handle_race_file

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


def all_races(request):
    races = Race.objects.all()

    context = {
        'races': races
    }

    return render(request, 'all_races.html', context)


def race_detail(request, slug):
    race = get_object_or_404(Race, slug=slug)
    results = Result.objects.filter(race_id=race.id)

    context = {
        'race': race,
        'results': results
    }

    return render(request, 'race_detail.html', context)


@login_required
def upload_race(request):
    return render(request, 'upload.html')


def upload_race_file(request):
    if request.method == "POST":
        form = UploadRaceForm(request.POST, request.FILES)
        if form.is_valid():
            handle_race_file(request.FILES["file"])
            # return something here, potentially
    else:
        form = UploadRaceForm()
    return render(request, 'upload_partial.html', {"form": form})
