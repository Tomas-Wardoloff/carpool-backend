from rest_framework import serializers

from phonenumber_field.serializerfields import PhoneNumberField

from authentication.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Class to serialize and deserialize CustomUser instances.
    
    Meta:
        model (CustomUser): The model that this serializer is associated with.
        fields (list): The list of fields to include in the serialized representation.
        read_only_fields (list): The list of fields that are read-only.

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
        