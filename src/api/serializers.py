from rest_framework import serializers

from phonenumber_field.serializerfields import PhoneNumberField

from authentication.models import CustomUser
from trip.models import State, City, Vehicle


class CreateCustomUserSerializer(serializers.ModelSerializer):
    """
    This serializer handles the serialization of CustomUser instances for the create and update actions,
    including all fields except for the django default fields.

    Methods:
        create(validated_data):
            Creates a new CustomUser instance with the provided validated data.
            Ensures the password is hashed before saving.

        update(instance, validated_data):
            Updates an existing CustomUser instance with the provided validated data.
            Ensures the password is hashed if it is included in the validated data.
    """
    phone_number = PhoneNumberField(region='AR')   
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'birth_date', 'about_me', 'document_number', 'phone_number']
        read_only_fields = ['id']
        
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
    

class ListCustomUserSerializer(serializers.ModelSerializer):
    """
    This serializer handles the serialization of CustomUser instances for the list action,
    including only the 'id', 'email', 'first_name' and 'last_name' field to avoid exposing sensitive data.
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'email', 'first_name', 'last_name']


class DetailCustomUserSerializer(serializers.ModelSerializer):
    """
    This serializer handles the serialization of CustomUser instances for the retrieve action,
    including detailed fields but excluding sensitive data.
    """
    phone_number = PhoneNumberField(region='AR')   
    
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'birth_date', 'about_me', 'document_number', 'phone_number']


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


class VehicleSerializer(serializers.ModelSerializer):
    """
    Class to serialize and deserialize Vehicle instances.
    Excluded fields: 'owner'.
    """
    class Meta:
        model = Vehicle
        fields = ['id', 'license_plate', 'brand', 'model']
        read_only_fields = ['id', 'owner']
        