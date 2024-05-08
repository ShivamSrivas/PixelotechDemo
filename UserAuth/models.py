from django.db import models
from django.contrib.postgres.fields import ArrayField

class UserProfileDetail(models.Model):
    """
    Model to represent user profile.
    """
    id = models.AutoField(primary_key=True, unique=True)
    Name = models.CharField(max_length=100)
    Email = models.EmailField(unique=True)
    PhoneNumber = models.CharField(max_length=15)
    Password = models.CharField(max_length=128) 
    Rejected = ArrayField(models.CharField(max_length=128), null=True, blank=True)
    Accepted = ArrayField(models.CharField(max_length=128), null=True, blank=True)
    creation_date = models.DateField(auto_now_add=True)
    creation_time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.Name

class EmailVerification(models.Model):
    """
    Model to store OTP for email verification.
    """
    Email = models.EmailField(unique=False)
    Otp = models.CharField(max_length=6)
    Date = models.DateField(auto_now_add=True)
    Time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.Email}"

class Product(models.Model):
    UniqueNumber = models.CharField(max_length=4, unique=True, verbose_name='Unique Number')
    Url = models.URLField(verbose_name='URL')

    def __str__(self):
        return f"Product {self.UniqueNumber}"

class PhoneVerification(models.Model):
    """
    Model to store OTP for phone number verification.
    """
    PhoneNumber = models.CharField(max_length=15, unique=False)
    Otp = models.CharField(max_length=6)
    Date = models.DateField(auto_now_add=True)
    Time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.PhoneNumber}"
