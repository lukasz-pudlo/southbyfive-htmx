from django.core.management import BaseCommand
import random
from datetime import date, timedelta

from races.models import Season, Race, Runner, Result


class Command(BaseCommand):
    help = "Populate the database with mock runners and results"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=100,
            help="Number of runners to create"
        )

    def create_seasons(self, index):
        seasons = ['2324', '2425', '2526']

        for season in seasons:
            season_object = Season.objects.create(
                season=season
            )
