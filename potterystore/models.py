from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name 
# this model contains three attributes, the user, the name and the email. The user attribute links the 'Customer' model to a single 'User' (imported built in Django feature) object. I'm making this field optional for my guest checkout feature.
#  The name attribute stores the name of the customer. I've allowed this to be left blank with null=True for guest checkouts
# The email attribute stores the email of the customer, I've set both to a max character length of 200 which might be too high, but you can never be too careful
# the str method returns to my admin interface, all of my Customer instances as a string representation of its name attribute. So all of my customers are hopefully represented by their names

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()

    def __str__(self):
        return str(self.name)
# identical model except it must return the name of the product (no null=True) because that's key information
# the price can be stored as floating-point number in case the product has a decimal point. I justify this as good practise although I don't intend to sell pottery for £45.72
# Once again it returns a string representation of the name of the product for database purposes



    
