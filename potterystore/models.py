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
    image = models.ImageField(null=True, blank=True)
    def __str__(self):
        return str(self.name)
# identical model except it must return the name of the product (no null=True) because that's key information
# the price can be stored as floating-point number in case the product has a decimal point. I justify this as good practise although I don't intend to sell pottery for £45.72
# Once again it returns a string representation of the name of the product for database purposes

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)
# customer is a ForeignKey field. This field creates a link between the parent model (Customer) and the child model (Order). This lets me track multiples instances of the child Order model to one parent Customer model. So one customer can now place multiple orders, all of which are tracked. 
# Also, if the referenced parent 'Customer' model is deleted, the 'customer' field is deleted

# date ordered records the date and time of the order being placed, set to the current date and time, which cannot be changed
# complete indicates whether an order has been completed
# transaction_id creates a field to store a unique transaction ID for the order, this is optional
# the str method returns the id to the admin database as a string representation

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

# Here we're creating a class for our ordered product, linking it to the Product and Order classes, noting the quantity and date the product was added to the order
# This will store information in our database that will be used by our cart page.

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=True, blank=True)
    postcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    
    # For my shipping adddress class, I'm making the city optional as not all customer's live in cities

