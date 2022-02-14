from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django_countries.fields import CountryField

import secrets
# Create your models here.
CATEGORY_CHOICE = (
    ('T Shirt','T Shirt'),
    ('Laptop','Laptop'),
    ('Shoe','Shoe'),
    ('Book','Book'),
    ('Bag','Bag'),
)

class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True,null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICE)
    description = models.TextField(blank=True, null= True)
    date_created = models.DateTimeField(default=datetime.now(),blank=True)
    image = models.ImageField(default="img/thumbnail.png")



    def __str__(self):
        return self.title

class Order_item(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.item.title}'

    def gettotalprice(self):
        return self.quantity * self.item.price
         
    def getdiscount_price(self):
        return self.quantity * self.item.discount_price
      
    def get_final_price(self):
        if self.item.discount_price:
            return self.getdiscount_price()
        return self.gettotalprice()


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    items = models.ManyToManyField(Order_item)
    start_date = models.DateTimeField(default=datetime.now(),blank=True)
    ordered_date= models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress',on_delete=models.SET_NULL,blank=True,null=True)
    payment = models.ForeignKey('Payment',on_delete=models.SET_NULL,blank=True,null=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for i in self.items.all():
            total += i.get_final_price()
        return total

class BillingAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    street_address = models.CharField(max_length=200)
    apartment_address = models.CharField(max_length=200)
    country = CountryField(multiple=False)
    zip = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,blank=True,null=True)
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=datetime.now(),blank=True)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args,**kwargs)
    
    def amount_value(self) -> int:
        return self.amount *100