from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import Customusermanager

# Create your models here.

class User(AbstractUser):

    username = None

    email = models.CharField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = Customusermanager()

    
