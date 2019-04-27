from django.db import models
from django.contrib.auth.models import User
from .choices import CHOICES
# Create your models here.
class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.TextField()
    rating=models.FloatField(default=0.0)
    def __str__(self):
        return self.text
class Menu(models.Model):
    name=models.CharField(max_length=30)
    image=models.ImageField()
    description=models.TextField()
    price=models.FloatField(default=0.0)
    veg=models.BooleanField(default=False)
    def __str__(self):
        return self.name
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
    phone_number=models.IntegerField(default=0)
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    image=models.ImageField()
    location=models.CharField(max_length=50)
    city=models.CharField(max_length=20)
    state=models.CharField(max_length=20,choices=CHOICES)
    about=models.TextField()
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="user_profile")
    cart =models.ManyToManyField(Menu,blank=True)
    fav_restraunts=models.ManyToManyField(Restraunt,blank=True,related_name="fav_restraunts")
    customer=models.BooleanField(default=True)
    my_restraunts=models.ManyToManyField(Restraunt,blank=True,related_name="my_restraunts")
    phone_number=models.IntegerField(default=0)

class Restraunt_owner(models.Model):
    image=models.ImageField()
    user=models.OneToOneField(User,on_delete=models.CASCADE,blank=True)
    restraunt=models.ManyToManyField(Restraunt)
    def __str__(self):
        return self.user.username

class new_request(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    approved=models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
class order_detail(models.Model):
    restraunt=models.ForeignKey(Restraunt,on_delete=models.CASCADE,)
    menu=models.ForeignKey(Menu,on_delete=models.CASCADE)
    user_profile=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    delivered=models.BooleanField(default=False)
class Delivery(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    order=models.ManyToManyField(order_detail,blank=True)
    phone_number=models.IntegerField(default=0)
    is_available=models.BooleanField(default=True)





