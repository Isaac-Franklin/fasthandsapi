from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserRegisterModel(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    Fullname = models.CharField(max_length=200)
    Email = models.EmailField(max_length=254)
    PhoneNumber = models.CharField(max_length=200)
    Skill = models.CharField(max_length=300)
    Location = models.CharField(max_length=200)
    NIN =models.CharField(max_length=200)
    Password =models.CharField(max_length=200)
    ConfirmPassword =models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-edited_at', '-created_at']
        
