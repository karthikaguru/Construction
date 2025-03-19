from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Core user fields
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    # Authorization field
    is_authorized = models.BooleanField(default=False)

    # Role-based field using choices
 
    ADMIN = 'ADMIN'
    CLIENT = 'CLIENT'
    TEAM_USER = 'TEAM_USER'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (CLIENT, 'Client'),
        (TEAM_USER, 'Team User'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CLIENT)


    # Set related_name for groups and user_permissions to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Unique related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Unique related_name
        blank=True
    )

    def __str__(self):
        return self.username
