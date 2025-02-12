from datetime import datetime

from rest_framework import serializers

from phonenumber_field.serializerfields import PhoneNumberField

from .models import CustomUser


class CustomUserCreateSerializer(serializers.ModelSerializer):
    """
    This serializer handles the serialization of CustomUser instances for the create, update and partial update actions
    including all fields except for the django default fields.

    Methods:
        validate_profile_picture(value): Ensures the profile picture does not exceed 2MB.

        validate_document_number(value): Ensures the document number is 8 digits long and is a positive integer.

        validate_birth_date(value): Ensures the user is at least 18 years old and the birth date is not more than 100 years ago.

        create(validated_data): Ensures the password is hashed before saving.

        update(instance, validated_data): Ensures the password is hashed if it is included in the validated data.
    """

    phone_number = PhoneNumberField(region="AR")

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "birth_date",
            "about_me",
            "document_number",
            "phone_number",
            "profile_picture",
        ]
        read_only_fields = ["id"]

    def validate_profile_picture(self, value):
        file_size = value.size
        if file_size > 5 * 1024 * 1024:
            raise serializers.ValidationError("La imagen no puede superar los 2MB")

    def validate_document_number(self, value):
        if len(value) != 8 or int(value) <= 0 or not value.isdigit():
            raise serializers.ValidationError("Número de documento inválido.")

    def validate_birth_date(self, value):
        if value.year - datetime.today.year < 18:  # CHECK VALUE.YEAR
            raise serializers.ValidationError(
                "Los usuarios deben ser mayores de 18 años."
            )
        if value.year - datetime.today.year > 100:
            raise serializers.ValidationError("Fecha de nacimiento inválida.")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)
        return super().update(instance, validated_data)


class CustomUserListSerializer(serializers.ModelSerializer):
    """
    This serializer handles the serialization of CustomUser instances for the list action,
    including only the 'id', 'first_name' and 'last_name' field to avoid exposing sensitive data.
    """

    class Meta:
        model = CustomUser
        fields = ["id", "first_name", "last_name"]
        read_only_fields = ["id", "first_name", "last_name"]
