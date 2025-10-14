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
        # For season 2025/2026, enter 2526
        seasons = ['2324', '2425', '2526']

        for season in seasons:
            self.create_seasons(season)

        self.create_races()

    def create_seasons(self, season):
        season_object = Season.objects.update_or_create(
            season=season
        )
        return season_object

    def create_races(self, *args, **kwargs):
        seasons = Season.objects.all()
        print(f"Managed to retrieve seasons: {seasons}")
        parks = ['KP', 'LP', 'RG', 'PP', 'BP', 'QP']
        for season in seasons:
            print(f"Creating races for season {season}")
            for park in parks:
                race_object = Race.objects.update_or_create(
                    park=park,
                    season=season
                )
        return race_object
