from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import State, City


class TestStateModel(TestCase):
    def setUp(self):
        self.state = State.objects.create(
            name="Buenos Aires", abbreviation="BA", country="Argentina"
        )

    def test_create_state(self):
        state = State.objects.create(
            name="Santa Fe", abbreviation="SF", country="Argentina"
        )
        self.assertEqual(state.name, "Santa Fe")
        self.assertEqual(state.abbreviation, "SF")
        self.assertEqual(state.country, "Argentina")

    def test_name_is_required(self):
        with self.assertRaises(ValidationError):
            State.objects.create(abbreviation="BA", country="Argentina")

    def test_abbreviation_is_required(self):
        with self.assertRaises(ValidationError):
            State.objects.create(name="Buenos Aires", country="Argentina")

    def test_country_is_required(self):
        with self.assertRaises(ValidationError):
            State.objects.create(name="Buenos Aires", abbreviation="BA")

    def test_create_state_with_cities(self):
        city1 = City.objects.create(
            name="Rosario", latitude=-32.944242, longitude=-60.650538, state=self.state
        )
        city2 = City.objects.create(
            name="Santa Fe", latitude=-31.63333, longitude=-60.7, state=self.state
        )
        self.assertEqual(self.state.cities.count(), 2)

    def test_delete_state_with_cities(self):
        pass

    def test_access_cities_from_state(self):
        city1 = City.objects.create(
            name="Rosario", latitude=-32.944242, longitude=-60.650538, state=self.state
        )
        city2 = City.objects.create(
            name="Santa Fe", latitude=-31.63333, longitude=-60.7, state=self.state
        )
        self.assertEqual(list(self.state.cities.all()), [city1, city2])

    def test_name_is_title_cased(self):
        self.assertEqual(self.state.name, "Buenos Aires")

    def test_abbreviation_is_upper_cased(self):
        self.assertEqual(self.state.abbreviation, "BA")

    def test_country_is_title_cased(self):
        self.assertEqual(self.state.country, "Argentina")

    def test_name_abbr_country_unique_together(self):
        with self.assertRaises(ValidationError):
            State.objects.create(
                name="Buenos Aires", abbreviation="BA", country="Argentina"
            )

    def test_str_method(self):
        self.assertEqual(str(self.state), "Buenos Aires, Argentina")
