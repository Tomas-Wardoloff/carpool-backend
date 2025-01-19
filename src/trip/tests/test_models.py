from django.test import TestCase
from django.core.exceptions import ValidationError

from ..models import State


class TestStateModel(TestCase):
    def setUp(self):
        self.state = State.objects.create(name='Buenos Aires', abbreviation='BA', country='Argentina')
    
    def test_create_state(self):
        state = State.objects.create(name="California", abbreviation="CA", country="United States")
        self.assertEqual(state.name, "California")
        self.assertEqual(state.abbreviation, "CA")
        self.assertEqual(state.country, "United States")
    
    def test_name_is_required(self):
        with self.assertRaises(ValidationError):
            State.objects.create(abbreviation='BA', country='Argentina')
            
    def test_abbreviation_is_required(self):
        with self.assertRaises(ValidationError):
            State.objects.create(name='Buenos Aires', country='Argentina')
            
    def test_country_is_required(self):
        with self.assertRaises(ValidationError):
            State.objects.create(name='Buenos Aires', abbreviation='BA')
            
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
        