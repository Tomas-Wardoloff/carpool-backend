import re

from datetime import timedelta, datetime

from django.db import models
from django.core.exceptions import ValidationError

from authentication.models import CustomUser


class State(models.Model):
    """
    State model representing a state in the system.
    
    Attributes:
        - name (CharField): The name of the state.
        - abbreviation (CharField): The abbreviation of the state.
        - country (CharField): The country of the state.
    
    Attributes inherits from Model:
        - id (AutoField): The primary key for the state.
        
    Methods:
        - __str__: Returns a string representation of the state.
    """
    name = models.CharField(max_length=100, verbose_name="Nombre")
    abbreviation = models.CharField(max_length=2, verbose_name="Abreviatura")
    country = models.CharField(max_length=100, verbose_name="País")
    
    def __str__(self):
        return f"{self.name}, {self.country}"

class City(models.Model):
    """
    City model representing a city in the system.
    
    Attributes:
        - name (CharField): The name of the city.
        - latitude (FloatField): The latitude of the city.
        - longitude (FloatField): The longitude of the city.
        - state (CharField): The state of the city.
    
    Attributes inherits from Model:
        - id (AutoField): The primary key for the city.
    
    Methods:
        - __str__: Returns a string representation of the city.
        - clean: Validates the latitude and longitude of the city.
    """
    name = models.CharField(max_length=100, verbose_name='Nombre')
    latitude = models.FloatField(verbose_name='Latitud')
    longitude = models.FloatField(verbose_name='Longitud')
    state = models.ForeignKey(State, related_name='cities', on_delete=models.CASCADE, verbose_name='Provincia')
    
    def clean(self):
        pass
    
    def __str__(self):
        return f"{self.name}, {self.state}"


class Vehicle(models.Model):
    """
    Vehicle model representing a vehicle in the system.
    
    Attributes:
        - owner (ForeignKey): The owner of the vehicle.
        - license_plate (CharField): The license plate of the vehicle.
        - brand (CharField): The brand of the vehicle.
        - model (CharField): The model of the vehicle.
        
    Attributes inherits from Model:
        - id (AutoField): The primary key for the vehicle.
        
    Methods:    
        - __str__: Returns a string representation of the vehicle.
        - clean: Validates the license plate of the vehicle and if the vehicle is already register for that User.
    """
    owner = models.ForeignKey(CustomUser, related_name='vehicles', on_delete=models.CASCADE, verbose_name='Propietario')
    license_plate = models.CharField(max_length=7, verbose_name='Patente', unique=True)
    brand = models.CharField(max_length=50, verbose_name='Marca')
    model = models.CharField(max_length=50, verbose_name='Modelo')
    
    def clean(self):
        if not re.match(r'^(?:[A-Z]{3}\d{3}|[A-Z]{2}\d{3}[A-Z]{2})$', self.license_plate):
            raise ValidationError('Patente invalida') # check if the license plate FORMAT: ABC123 or AB123CD before save
        if self.owner.vehicles.license_plate == self.license_plate:
            raise ValidationError('El usuario ya cuenta con un vehículo registrado con esa patente') # check if the user already has a vehicle with the same license plate before save
    
    def __str__(self):
        return f'{self.brand} {self.model} {self.license_plate}'""


class Trip(models.Model):
    """
    Trip model representing a trip in the system.
    
    Attributes:
        - origin_city (ForeignKey): The origin city of the trip.
        - destination_city (ForeignKey): The destination city of the trip.
        - departure_date (DateField): The departure date of the trip.
        - departure_time (TimeField): The departure time of the trip.
        - vehicle (ForeignKey): The vehicle of the trip.
        - participants (ManyToManyField): The participants of the trip.
    
    Attributes inherits from Model:
        - id (AutoField): The primary key for the trip.
        
    Methods:
        - __str__: Returns a string representation of the trip.
        - clean: Validates the origin city, destination city, departure date, and departure time of the trip.
    """
    origin_city = models.ForeignKey(City, related_name='trips_from', on_delete=models.CASCADE, verbose_name='Ciudad de origen') 
    destination_city = models.ForeignKey(City, related_name='trips_to', on_delete=models.CASCADE, verbose_name='Ciudad de destino') 
    departure_date = models.DateField(verbose_name='Fecha de salida')
    departure_time = models.TimeField(verbose_name='Hora de salida')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, verbose_name='Vehículo')
    participants = models.ManyToManyField(CustomUser, related_name='trips', through='TripParticipant', verbose_name='Participantes')

    def clean(self):
        if self.origin_city == self.destination_city:
            raise ValidationError('La ciudad de origen no puede ser la misma que la ciudad de destino')
        
        departure_datetime = datetime.combine(self.departure_date, self.departure_time)
        if departure_datetime < datetime.now():
            raise ValidationError('La fecha de salida no puede ser anterior a la fecha actual')
        
        one_year_from_now = datetime.now() + timedelta(days=365)
        if departure_datetime > one_year_from_now:
            raise ValidationError('La fecha de salida no puede ser superior a un año desde la fecha')
        
    def __str__(self):
        return f'from {self.origin_city} to {self.destination_city} on {self.departure_date}'
    

class TripParticipant(models.Model):
    """
    TripParticipant model representing a participant in a trip in the system.
    
    Attributes:
        - user (ForeignKey): The user of the participant.
        - trip (ForeignKey): The trip of the participant.
        - role (CharField): The role of the participant.
    
    Attributes inherits from Model:
        - id (AutoField): The primary key for the participant.
    
    Methods:
        - __str__: Returns a string representation of the participant.
        - clean: Validates that there is only one driver per trip, 
        that the driver is the owner of the vehicle used in the trip
        and that the user does not have another trip scheduled for the same date.
    
    Meta:
        - unique_together: The user and trip of the participant must be unique together.
    """
    user = models.ForeignKey(CustomUser, related_name='user_trips',on_delete=models.CASCADE, verbose_name='Usuario')
    trip = models.ForeignKey(Trip, related_name='trip_participants', on_delete=models.CASCADE, verbose_name='Viaje') 
    role = models.CharField(max_length=10, choices=[('driver', 'Driver'),('passenger', 'Passenger'),], verbose_name='Rol')

    def clean(self):
        if self.role == 'driver':
            if self.trip.participants.filter(role='driver').exists():
                raise ValidationError('Ya existe un conductor asignado para este viaje.') # check if there is already a driver in the trip before save

            if self.trip.vehicle.owner != self.user:
                raise ValidationError("Solo el dueño del vehículo puede ser el conductor") # check if the driver of the trip is the owner of the vehicle
            
        if self.user.trips.filter(departure_date=self.trip.departure_date, departure_time=self.trip.departure_time).exists():
            raise ValidationError('El usuario ya posee un viaje programado para esa fecha') # check if the user already has a trip scheduled for the same date before save
    
    def __str__(self):
        return f"{self.user.email} as {self.role} in trip {self.trip}"
    
    class Meta:
        unique_together = ('user', 'trip')
    