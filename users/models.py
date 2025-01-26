from django.db import models
from django.contrib.auth.models import AbstractUser
from config.model_utils.models import TimeStampModel

class User(AbstractUser):
    email=models.EmailField(unique=True)
    phone_number=models.CharField(unique=True, max_length=32)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username', 'phone_number']

    def __str__(self):
        return self.email
    
    
    


