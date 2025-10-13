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

    def handle(self, *args, **kwargs):
        seasons = ['2627', '2728', '2829']

        for season in seasons:
            self.create_seasons(season)

    def create_seasons(self, season):
        season_object = Season.objects.create(
            season=season
        )
        return season_object
