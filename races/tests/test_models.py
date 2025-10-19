from django.test import TestCase
from races.models import Runner


class RunnerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        Runner.objects.create(
            first_name='Lukasz',
            last_name='Pudlo',
            gender='M',
            participant_number=1,
            category='MS',
        )

    def setUp(self):
        # Runs before each test method
        # You can use this for data that might modified in tests
        print("setUp: Run once for every test method to set up clean data.")
        pass

    def test_first_name_label(self):
        runner = Runner.objects.get(id=1)
        field_label = runner._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        runner = Runner.objects.get(id=1)
        field_label = runner._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_gender_label(self):
        runner = Runner.objects.get(id=1)
        field_label = runner._meta.get_field('gender').verbose_name
        self.assertEqual(field_label, 'gender')

    def test_participant_number_label(self):
        runner = Runner.objects.get(id=1)
        field_label = runner._meta.get_field('participant_number').verbose_name
        self.assertEqual(field_label, 'participant number')

    def test_category_label(self):
        runner = Runner.objects.get(id=1)
        field_label = runner._meta.get_field('category').verbose_name
        self.assertEqual(field_label, 'category')

    def test_club_label(self):
        runner = Runner.objects.get(id=1)
        field_label = runner._meta.get_field('club').verbose_name
        self.assertEqual(field_label, 'club')

    def test_full_name_is_first_name_space_last_name(self):
        runner = Runner.objects.get(id=1)
        expected_full_name = f"{runner.first_name} {runner.last_name}"
        self.assertEqual(str(runner), expected_full_name)
