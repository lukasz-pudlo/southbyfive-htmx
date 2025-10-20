import logging
from django.test import TestCase
from django.urls import reverse
from races.models import Season, Race, Runner, Result
from races.utils import handle_race_file
from southbyfivehtmx.settings import BASE_DIR

logger = logging.getLogger(__name__)


class RaceResultListView(TestCase):
    def setUp(self):
        filepath = f"{BASE_DIR}/races/tests/resources/kings.xlsx"
        season = Season.objects.create(
            season='2526'
        )
        handle_race_file(filepath, season)

    def test_get_race_list(self):
        # Verify the race was created
        race = Race.objects.filter(slug='kp-2526').first()
        self.assertIsNotNone(race, "Race with slug 'kp-2526' was not created")

        response = self.client.get(
            reverse('race-detail', kwargs={'slug': 'kp-2526'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'race_detail.html')

    def test_results_in_ascending_time_order(self):
        race = Race.objects.filter(slug='kp-2526').first()
        results = Result.objects.filter(race=race.id)

        next_result = None

        for index, result in enumerate(results):
            if index < len(results) - 1:
                next_result = results[index + 1]
            else:
                next_result = None

            logger.debug(
                f"This result is {result} and next result is {next_result}")
            this_time = result.time
            if next_result is not None:
                next_time = next_result.time

            if next_result is not None:
                self.assertGreater(
                    next_time, this_time, 'Next result in the list is not greater than the previous result')
