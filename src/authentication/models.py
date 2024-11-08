from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name='Email', unique=True)
    birth_date = models.DateField(verbose_name='Fecha de nacimiento')
    about_me = models.TextField(max_length=500, blank=True, verbose_name='Descripcion')
    document_number = models.CharField(max_length=8, verbose_name='Número de documento')
    phone_number = PhoneNumberField(region='AR', verbose_name='Número de teléfono')
    # profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = CustomUserManager()
    
    def __str__(self) -> str:
        return self.email
    
    def clean(self):
        super.clean()
        
        if len(self.document_number) != 8 or int(self.document_number) <= 0 or not self.document_number.isdigit():
            raise ValidationError('Número de documento inválido.')

        if self.birth_date.year - datetime.today.year < 18:
            raise ValidationError('Los usuarios deben ser mayores de 18 años.')
        if self.birth_date.year - datetime.today.year > 100:
            raise ValidationError('Fecha de nacimiento inválida.')
    
    def save(self, *args, **kwargs):
        self.username = f"{self.first_name} {self.last_name}" # auto assign username
        super().save(*args, **kwargs)