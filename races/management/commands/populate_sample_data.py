from django.core.management import BaseCommand
import random
from datetime import date, timedelta
from faker import Faker

from races.models import Season, Race, Runner, Result
fake = Faker()


class Command(BaseCommand):
    help = "Populate the database with mock runners and results"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=100,
            help="Number of runners to create"
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating mock data"
        )

    def handle(self, *args, **options):
        count = options['count']
        clear = options['clear']

        if clear:
            print("Clearing existing data")
            Season.objects.all().delete()
            Runner.objects.all().delete()
            print("Existing data cleared")

        # For season 2025/2026, enter 2526
        seasons = ['2324', '2425', '2526']

        for season in seasons:
            self.create_seasons(season)

        self.create_races()

        runner_counter = 1
        for i in range(count):
            print(f"Printing runner number {i+1}")
            name = fake.name()
            self.create_runners(name)
            runner_counter += 1

        total_runners = runner_counter - 1
        print(f"Successfully created {total_runners} runners")

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

    def create_runners(self, name):
        gender_list = list(Runner.GENDER_CHOICES.keys())
        random_gender = random.choice(gender_list)
        print(
            f"Creating a runner with fake name {name} and gender {random_gender}")
        runner = Runner.objects.update_or_create(
            full_name=name,
            gender=random_gender
        )
        return runner
