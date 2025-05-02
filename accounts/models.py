from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (   
        ('victim', 'Victim'),
        ('counselor', 'Counselor'),
        ('admin', 'Admin'),
    )
    
    email=models.EmailField(unique=True)
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    user_type=models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    date_joined=models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_type']
    
    objects=CustomUserManager()
    
    def __str__(self):
        return self.email
    
    
class UserProfile(models.Model):
    user=models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_profile')
    phone=models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True)
    bio=models.TextField(blank=True, null=True)
    date_of_birth=models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.first_name}'s Profile"
    
    
class CounselorProfile(models.Model):
    user=models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='counselor_profile')
    specialization=models.CharField(max_length=100)
    years_of_experience=models.PositiveIntegerField(default=0)
    qualifications=models.TextField()
    
    def __str__(self):
        return f"{self.user.first_name}'s Counselor Profile"
    
    
    