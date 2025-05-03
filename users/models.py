from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

def validate_age(birth_date):
    today = date.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if age < 15:
        raise ValidationError('Users must be at least 15 years old to register (GDPR compliance).')

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, birth_date=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not birth_date:
            raise ValueError('The Birth Date field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, birth_date=birth_date, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, birth_date=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, birth_date, **extra_fields)

class User(AbstractUser):
    birth_date = models.DateField(validators=[validate_age])
    email = models.EmailField(unique=True)
    
    objects = UserManager()
    
    def __str__(self):
        return self.username
