from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    """
    Attributes:
        - email (EmailField): The email address of the user.
        - birth_date (DateField): The birth date of the user.
        - about_me (TextField): A short description about the user.
        - document_number (CharField): The document number of the user.
        - phone_number (PhoneNumberField): The phone number of the user.
        - profile_picture (ImageField): The profile picture of the user.

    Attributes inherits from AbstractUser:
        - username (CharField): The username of the user.
        - password (CharField): The password of the user.
        - first_name (CharField): The first name of the user.
        - last_name (CharField): The last name of the user.
        - is_superuser (BooleanField): Designates whether the user has all permissions without explicitly assigning them.
        - is_staff (BooleanField): Designates whether the user can access the admin site.
        - is_active (BooleanField): Designates whether the user account is active.
        - date_joined (DateTimeField): The date and time when the user account was created.
        - last_login (DateTimeField): The date and time when the user last logged in.

    Custom Manager:
        - objects (CustomUserManager): Custom manager for the CustomUser model.

    Methods:
        - __str__: Returns a string representation of the user.
        - save: Capitalizes the first and last name of the user and assigns the username.
    """

    email = models.EmailField(verbose_name="Email", unique=True)
    birth_date = models.DateField(
        verbose_name="Fecha de nacimiento", blank=True, null=True
    )
    about_me = models.TextField(max_length=500, blank=True, verbose_name="Descripcion")
    document_number = models.CharField(max_length=8, verbose_name="Número de documento")
    phone_number = PhoneNumberField(region="AR", verbose_name="Número de teléfono")
    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", blank=True, null=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        self.username = f"{self.first_name} {self.last_name}"  # auto assign username

        if self.profile_picture:
            self.profile_picture.name = f"{self.email}_profile_picture.{self.profile_picture.name.split('.')[-1]}"
        super().save(*args, **kwargs)
