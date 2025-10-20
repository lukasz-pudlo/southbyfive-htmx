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
        self.assertContains(response, 'kp-2526')
