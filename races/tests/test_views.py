from django.test import TestCase
from datetime import timedelta
from races.models import Season, Race, Runner, Result


class RaceDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create season
        cls.season = Season.objects.create(season='2425')

        # Create King's Park race for this season
        cls.race = Race.objects.create(
            park='KP',
            season=cls.season
        )

        # Create a few test runners
        cls.runner1 = Runner.objects.create(
            first_name='John',
            last_name='Doe',
            gender='M',
            participant_number='001',
            category='MS',
            club='Test Club A'
        )

        cls.runner2 = Runner.objects.create(
            first_name='Jane',
            last_name='Smith',
            gender='F',
            participant_number='002',
            category='FS',
            club='Test Club B'
        )

        # Create results for the race
        cls.result1 = Result.objects.create(
            race=cls.race,
            runner=cls.runner1,
            time=timedelta(minutes=25, seconds=30)
        )

        cls.result2 = Result.objects.create(
            race=cls.race,
            runner=cls.runner2,
            time=timedelta(minutes=27, seconds=15)
        )
