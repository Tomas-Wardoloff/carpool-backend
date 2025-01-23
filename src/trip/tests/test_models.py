from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import State, City


class TestStateModel(TestCase):
    def setUp(self):
        self.state = State.objects.create(name='Buenos Aires', abbreviation='BA', country='Argentina')
    
    def test_create_state(self):
        state = State.objects.create(name="Santa Fe", abbreviation="SF", country="Argentina")
        self.assertEqual(state.name, "Santa Fe")
        self.assertEqual(state.abbreviation, "SF")
        self.assertEqual(state.country, "Argentina")
    
    def test_name_is_required(self):
        with self.assertRaises(ValidationError):
            State.objects.create(abbreviation='BA', country='Argentina')
            
    def test_abbreviation_is_required(self):
        with self.assertRaises(ValidationError):
            State.objects.create(name='Buenos Aires', country='Argentina')
            
    def test_country_is_required(self):
        with self.assertRaises(ValidationError):
            State.objects.create(name='Buenos Aires', abbreviation='BA')
            
    def test_create_state_with_cities(self):
        city1 = City.objects.create(name='Rosario', latitude=-32.944242, longitude=-60.650538, state=self.state)
        city2 = City.objects.create(name='Santa Fe', latitude=-31.63333, longitude=-60.7, state=self.state)
        self.assertEqual(self.state.cities.count(), 2)
    
    def test_delete_state_with_cities(self):
        pass
        #city1 = City.objects.create(name='Rosario', latitude=-32.944242, longitude=-60.650538, state=self.state)
        #city2 = City.objects.create(name='Santa Fe', latitude=-31.63333, longitude=-60.7, state=self.state)
        #self.state.delete()
        #self.assertEqual(City.objects.filter(state=self.state).count(), 0)
        
    def test_access_cities_from_state(self):
        city1 = City.objects.create(name='Rosario', latitude=-32.944242, longitude=-60.650538, state=self.state)
        city2 = City.objects.create(name='Santa Fe', latitude=-31.63333, longitude=-60.7, state=self.state)
        self.assertEqual(list(self.state.cities.all()), [city1, city2])
    
    def test_name_is_title_cased(self):
        self.assertEqual(self.state.name, 'Buenos Aires')
        
    def test_abbreviation_is_upper_cased(self):
        self.assertEqual(self.state.abbreviation, 'BA')
    
    def test_country_is_title_cased(self):
        self.assertEqual(self.state.country, 'Argentina')
    
    def test_name_abbr_country_unique_together(self):
        with self.assertRaises(ValidationError):
            State.objects.create(name='Buenos Aires', abbreviation='BA', country='Argentina')

    def test_str_method(self):
        self.assertEqual(str(self.state), 'Buenos Aires, Argentina')
        

class TestCityModel(TestCase):
    def setUp(self):
        self.state = State.objects.create(name='Santa Fe', abbreviation='SF', country='Argentina')
        self.city = City.objects.create(name='Rosario', latitude=-32.944242, longitude=-60.650538, state=self.state)
    
    def test_create_city(self):
        city = City.objects.create(name='Santa Fe', latitude=-31.63333, longitude=-60.7, state=self.state)
        self.assertEqual(city.name, 'Santa Fe')
        self.assertEqual(city.latitude, -31.63333)
        self.assertEqual(city.longitude, -60.7)
        self.assertEqual(city.state, self.state)
        
    def test_name_is_required(self):
        with self.assertRaises(ValidationError):
            City.objects.create(latitude=-32.944242, longitude=-60.650538, state=self.state)
            
    def test_latitude_is_required(self):
        with self.assertRaises(ValidationError):
            City.objects.create(name='Rosario', longitude=-60.650538, state=self.state)
            
    def test_longitude_is_required(self):
        with self.assertRaises(ValidationError):
            City.objects.create(name='Rosario', latitude=-32.944242, state=self.state)
            
    def test_state_is_required(self):
        with self.assertRaises(ValidationError):
            City.objects.create(name='Rosario', latitude=-32.944242, longitude=-60.650538)
            
    def test_access_state_from_city(self):
        self.assertEqual(self.city.state, self.state)
    
    def test_update_city_state(self):
        state1 = State.objects.create(name='Buenos Aires', abbreviation='BA', country='Argentina')
        state2 = State.objects.create(name='Córdoba', abbreviation='CD', country='Argentina')
        city = City.objects.create(name='La Plata', latitude=-34.920494, longitude=-57.953565, state=state1)
        city.state = state2
        city.save()
        self.assertEqual(city.state, state2)
    
    def test_name_is_title_cased(self):
        self.assertEqual(self.city.name, 'Rosario')
        
    def test_str_method(self):
        self.assertEqual(str(self.city), 'Rosario, Santa Fe, Argentina')