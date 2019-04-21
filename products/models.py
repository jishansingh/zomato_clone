from django.db import models
from django.contrib.auth.models import User
from .choices import CHOICES
# Create your models here.
class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.TextField()
    rating=models.FloatField(default=0.0)
class Menu(models.Model):
    name=models.CharField(max_length=30)
    image=models.ImageField()
    description=models.TextField()
    price=models.FloatField(default=0.0)
    veg=models.BooleanField(default=False)
class Restraunt(models.Model):
    name=models.CharField(max_length=40)
    owner_name=models.CharField(max_length=40)
    image=models.ImageField()
    menu=models.ManyToManyField(Menu,blank=True)
    delivery_time=models.IntegerField(default=0)
    rating=models.FloatField(default=0.0)
    address=models.CharField(max_length=60)
    city=models.CharField(max_length=20)
    state=models.CharField(max_length=20,choices=CHOICES)
    votes=models.IntegerField(default=0)
    veg=models.BooleanField(default=False)
    mode_of_payment=models.CharField(max_length=30,default="")
    review=models.ManyToManyField(Review,blank=True)
    offer=models.CharField(max_length=30,blank=True)
    cuisines=models.CharField(max_length=20,blank=True)

class UserProfile(models.Model):
    image=models.ImageField()
    location=models.CharField(max_length=50)
    city=models.CharField(max_length=20)
    state=models.CharField(max_length=20,choices=CHOICES)
    about=models.TextField()
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    cart =models.ManyToManyField(Menu,blank=True)
    fav_restraunts=models.ManyToManyField(Restraunt,blank=True)

class Restraunt_owner(models.Model):
    image=models.ImageField()
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    restraunt=models.ManyToManyField(Restraunt)