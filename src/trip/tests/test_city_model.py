from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import State, City


class TestCityModel(TestCase):
    def setUp(self):
        self.state = State.objects.create(
            name="Santa Fe", abbreviation="SF", country="Argentina"
        )
        self.city = City.objects.create(
            name="Rosario", latitude=-32.944242, longitude=-60.650538, state=self.state
        )

    def test_create_city(self):
        self.assertEqual(self.city.name, "Rosario")
        self.assertEqual(self.city.latitude, -32.944242)
        self.assertEqual(self.city.longitude, -60.650538)
        self.assertEqual(self.city.state, self.state)

    def test_name_is_required(self):
        with self.assertRaises(ValidationError):
            City.objects.create(
                latitude=-32.944242, longitude=-60.650538, state=self.state
            )

    def test_latitude_is_required(self):
        with self.assertRaises(ValidationError):
            City.objects.create(name="Rosario", longitude=-60.650538, state=self.state)

    def test_longitude_is_required(self):
        with self.assertRaises(ValidationError):
            City.objects.create(name="Rosario", latitude=-32.944242, state=self.state)

    def test_state_is_required(self):
        with self.assertRaises(ValidationError):
            City.objects.create(
                name="Rosario", latitude=-32.944242, longitude=-60.650538
            )

    def test_access_state_from_city(self):
        self.assertEqual(self.city.state, self.state)

    def test_update_city_state(self):
        state1 = State.objects.create(
            name="Buenos Aires", abbreviation="BA", country="Argentina"
        )
        state2 = State.objects.create(
            name="Córdoba", abbreviation="CD", country="Argentina"
        )
        city = City.objects.create(
            name="La Plata", latitude=-34.920494, longitude=-57.953565, state=state1
        )
        city.state = state2
        city.save()
        self.assertEqual(city.state, state2)

    def test_name_is_title_cased(self):
        self.assertEqual(self.city.name, "Rosario")

    def test_str_method(self):
        self.assertEqual(str(self.city), "Rosario, Santa Fe, Argentina")
