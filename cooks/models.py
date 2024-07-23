from django.db import models
from django import forms
from django.contrib.auth.models import User

# from django.contrib.auth.hashers import make_password

class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=255, default="")
    subject = models.CharField(max_length=100, default="")
    message = models.CharField(max_length=200, default="")

    def __str__(self) -> str:
        return self.name

class Single(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="")
    password = models.CharField(max_length=100, default="default_password")
    email = models.CharField(max_length=255, default="")
    experience = models.IntegerField(default=2)
    speciality = models.CharField(max_length=255)
    dish = models.CharField(max_length=255)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    desc = models.CharField(max_length=2000, default="")
    photo = models.ImageField(upload_to="uploads/cook/images", default="")

    def __str__(self):
        return self.username.username

class TeamCook(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="")
    password = models.CharField(max_length=100, default="default_password")
    email = models.CharField(max_length=255, default="")
    teamName = models.CharField(max_length=50, default="")
    experience = models.IntegerField(default=2)
    people = models.IntegerField(default=2)
    speciality = models.CharField(max_length=255)
    dish = models.CharField(max_length=255)
    desc = models.CharField(max_length=2000, default="")
    photo = models.ImageField(upload_to="uploads/cook/images", default="")

    def __str__(self):
        return self.username.username

class Booking(models.Model):
    order_id= models.AutoField(primary_key=True)
    name=models.CharField(max_length=90)
    username=models.CharField(max_length=90,default='username')
    email=models.CharField(max_length=111)
    address=models.CharField(max_length=111)
    city=models.CharField(max_length=111)
    state=models.CharField(max_length=111)
    zip_code=models.CharField(max_length=111)
    phone=models.CharField(max_length=10,default="")
    cookTime=models.DateField()
    time=models.TimeField()
    occasion = models.CharField(max_length=255)
    speciality = models.CharField(max_length=255)
    dish = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Payment(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, choices=(('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')))

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.status}"
