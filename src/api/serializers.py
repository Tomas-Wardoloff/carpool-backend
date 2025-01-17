import re
from datetime import datetime, timedelta

from rest_framework import serializers

from phonenumber_field.serializerfields import PhoneNumberField

from authentication.models import CustomUser
from trip.models import State, City, Vehicle, Trip, TripParticipant, TripJoinRequest


class CustomUserCreateSerializer(serializers.ModelSerializer):
    """
    This serializer handles the serialization of CustomUser instances for the create, update and partial update actions
    including all fields except for the django default fields.

    Methods:
        validate_profile_picture(value):
            Ensures the profile picture does not exceed 5MB.
    
        create(validated_data):
            Ensures the password is hashed before saving.

        update(instance, validated_data):
            Ensures the password is hashed if it is included in the validated data.
    """
    phone_number = PhoneNumberField(region='AR')   
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'birth_date', 'about_me', 'document_number', 'phone_number', 'profile_picture']
        read_only_fields = ['id']
        
    def validate_profile_picture(self, value):
        file_size = value.size
        if file_size > 5*1024*1024:
            raise serializers.ValidationError('La imagen no puede superar los 2MB')
    
    def validate_document_number(self, value):
        if len(value) != 8 or int(value) <= 0 or not value.isdigit():
            raise serializers.ValidationError('Número de documento inválido.')
        
    def validate_birth_date(self, value):        
        if value.year - datetime.today.year < 18: # CHECK VALUE.YEAR
            raise serializers.ValidationError('Los usuarios deben ser mayores de 18 años.')
        if value.year - datetime.today.year > 100:
            raise serializers.ValidationError('Fecha de nacimiento inválida.')
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)
    

class CustomUserListSerializer(serializers.ModelSerializer):
    """
    This serializer handles the serialization of CustomUser instances for the list action,
    including only the 'id', 'first_name' and 'last_name' field to avoid exposing sensitive data.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name']
        read_only_fields = ['id', 'first_name', 'last_name']


class CustomUserDetailSerializer(serializers.ModelSerializer):
    """
    This serializer handles the serialization of CustomUser instances for the retrieve action,
    including detailed fields but excluding sensitive data.
    """
    phone_number = PhoneNumberField(region='AR')   
    
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'birth_date', 'about_me', 'document_number', 'phone_number']
        read_only_fields = ['email', 'first_name', 'last_name', 'birth_date', 'about_me', 'document_number', 'phone_number']


class StateSerializer(serializers.ModelSerializer):
    """
    Class to serialize and deserialize State instances.
    Excluded fields: 'country'.
    """
    class Meta:
        model = State
        fields = ['id', 'name', 'abbreviation']
        read_only_fields = ['id', 'name', 'abbreviation']  
    
        
class CitySerializer(serializers.ModelSerializer):
    """
    Class to serialize and deserialize City instances.
    No excluded fields.
    """
    state = StateSerializer()
    
    class Meta:
        model = City
        fields = ['id', 'name', 'latitude', 'longitude', 'state']
        read_only_fields = ['id', 'name', 'latitude', 'longitude', 'state']


class VehicleDetailSerializer(serializers.ModelSerializer):
    """
    Serializer class for creating and updating Vehicle instances.

    This serializer handles the serialization and deserialization of Vehicle instances
    for the create, retrieve and update actions, ensuring that all necessary fields are included.
    Excluded fields: 'owner'.
    """
    class Meta:
        model = Vehicle
        fields = ['id', 'license_plate', 'brand', 'model']
        read_only_fields = ['id']

    def validate_license_plate(self, value):
        if not re.match(r'^(?:[A-Z]{3}\d{3}|[A-Z]{2}\d{3}[A-Z]{2})$', value):
            raise serializers.ValidationError('Patente invalida') # check license plate FORMAT: ABC123 or AB123CD 
        return value

    def validate(self, data):
        license_plate = data.get('license_plate')
        owner = self.context['request'].user

        if Vehicle.objects.filter(owner=owner, license_plate=license_plate).exists():
            raise serializers.ValidationError('El usuario ya cuenta con un vehículo registrado con esa patente') # check if the user already has a vehicle with the same license plate before save
        return data
        

class VehicleListSerializer(serializers.ModelSerializer):
    """
    Serializer class for listing Vehicle instances.

    This serializer handles the serialization of Vehicle instances for the list action,
    including only the 'id', 'brand', and 'model' fields to avoid exposing sensitive data.
    """
    class Meta:
        model = Vehicle
        fields = ['id', 'brand', 'model']
        read_only_fields = ['id', 'brand', 'model']


class TripParticipantDetailSerializer(serializers.ModelSerializer):
    """
    Serializer class for creating and updating TripParticipant instances.

    This serializer handles the serialization and deserialization of TripParticipant instances
    for the create, retrieve and update actions.
    """
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())

    class Meta:
        model = TripParticipant
        fields = ['id', 'trip', 'role']   
        read_only_fields = ['id']

    def validate_trip(self, value):
        if not Trip.objects.filter(id=value).exists():
            raise serializers.ValidationError('El viaje especificado no existe')
        return value 

    def validate_role(self, value):
        if value not in ('passanger', 'driver'):
            raise serializers.ValidationError('El rol especificado es invalido')
        return value


class TripParticipantListSerializer(serializers.ModelSerializer):
    """
    Serializer class for listing TripParticipant instances.

    This serializer handles the serialization of TripParticipant instances for the list action,
    including fields that provide an overview of the participant's involvement in the trip.
    """
    user = serializers.SlugRelatedField(slug_field='first_name', queryset=CustomUser.objects.all())
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())

    class Meta:
        model = TripParticipant
        fields = ['id', 'user', 'role', 'trip']
        read_only_fields = ['id', 'user', 'role', 'trip']
        

class TripDetailSerializer(serializers.ModelSerializer):
    """
    Serializer class for creating and updating Trip instances.

    This serializer handles the serialization and deserialization of Trip instances
    for the create, retrieve and update actions.
    """
    origin_city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    destination_city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    vehicle = serializers.PrimaryKeyRelatedField(queryset=Vehicle.objects.all())

    class Meta:
        model = Trip
        fields = ['id', 'origin_city', 'destination_city', 'departure_time', 'pet_allowed', 'smoking_allowed', 'kids_allowed', 'vehicle']
        read_only_fields = ['id']

    def validate_departure_date(self, value):
        one_year_from_now = datetime.now().date() + timedelta(days=365)
        if value > one_year_from_now:
            raise serializers.ValidationError('La fecha de salida no puede ser superior a un año desde la fecha actual')
        return value

    def validate(self, data):
        departure_date = data.get('departure_date')
        departure_time = data.get('departure_time')

        if data.get('origin_city') == data.get('destination_city'):
            raise serializers.ValidationError('La ciudad de origen y de destino no puede ser la misma ciudad') 
        if datetime.combine(departure_date, departure_time) < datetime.now():
            raise serializers.ValidationError('La fecha de salida no puede ser anterior a la fecha actual')
        return data


class TripListSerializer(serializers.ModelSerializer):
    """
    Serializer class for listing Trip instances.

    This serializer handles the serialization of Trip instances for the list action,
    including fields that provide an overview of the trip.
    """
    origin_city = serializers.StringRelatedField()
    destination_city = serializers.StringRelatedField()
    vehicle = VehicleListSerializer()
    participants = TripParticipantListSerializer(many=True)

    class Meta:
        model = Trip
        fields = ['id', 'origin_city', 'destination_city', 'departure_date', 'departure_time', 'pet_allowed', 'smoking_allowed', 'kids_allowed', 'vehicle', 'participants']
        read_only_fields = ['id', 'origin_city', 'detination_city', 'departure_date', 'departure_time', 'pet_allowed', 'smoking_allowed', 'kids_allowed', 'vehicle', 'participants']


class TripJoinRequestSerializer(serializers.ModelSerializer):
    """
    Seriliazer class for creating and updating TripJoinRequest instances.
    """
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    trip = serializers.PrimaryKeyRelatedField(queryset=Trip.objects.all())
    
    class Meta:
        model = TripJoinRequest
        fields = ['id', 'user', 'trip', 'status']
        read_only_fields = ['id']
        
    def validate_status(self, value):
        if value not in ('pending', 'accepted', 'rejected'):
            raise serializers.ValidationError('El estado especificado es invalido')
        return value
    
    def validate(self, data):
        user = data.get('user')
        trip = data.get('trip')
        
        if TripJoinRequest.objects.filter(user=user, trip=trip).exists():
            raise serializers.ValidationError('Ya existe una solicitud de unión para dicho viaje')
        if trip.creator == user:
            raise serializers.ValidationError('El creador del viaje no puede solicitar unirse a su propio viaje')
        return data
    