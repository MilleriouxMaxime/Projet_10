from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

def validate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if age < 15:
        raise ValidationError('Users must be at least 15 years old to register (GDPR compliance).')

class User(AbstractUser):
    birth_date = models.DateField(validators=[validate_age])
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.username
