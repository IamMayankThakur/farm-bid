from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class BuyerProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class SellerProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    aadhar_no = models.CharField(max_length=12)
    rating = models.IntegerField(null=True, blank=True)


class Category(models.Model):
    name = models.CharField()


class Item(models.Model):
    name = models.TextField(max_length=512, blank=False)
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE)
    buyer = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    costSold = models.FloatField(blank=True)
    basePrice = models.FloatField(blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Rating(models.Model):
    rated_by = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE)
    rated_to = models.ForeignKey(SellerProfile, on_delete=models.CASCADE)
    rated_on = models.ForeignKey(Item, on_delete=models.CASCADE)
    rating = models.IntegerField()


class Bid(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    current_highest = models.FloatField()
    current_bidder = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
