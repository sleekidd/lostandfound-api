from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')], blank=True)

    # Add custom fields here, if needed
    
    def __str__(self):
        return self.username

class LostItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Other fields...

class FoundItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # Other fields...
