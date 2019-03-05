from django.db import models
from django.contrib.auth.models import User


class BuyerProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class SellerProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    aadhar_no = models.CharField(max_length=12)
    rating = models.DecimalField(null=True, blank=True, max_digits=4, decimal_places=2)
    total_ratings = models.IntegerField(default=0)
    n_ratings = models.IntegerField(default=0)


class Category(models.Model):
    name = models.CharField(max_length = 256)


class Item(models.Model):
    name = models.CharField(max_length=50, blank=False)
    quantity = models.IntegerField(default=1)
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE)
    buyer = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE, null=True, blank=True)
    time = models.DateTimeField(auto_now=True)
    cost_sold = models.FloatField(blank=True, null=True)
    base_price = models.FloatField(blank=False, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Rating(models.Model):
    rated_on = models.ForeignKey(Item, on_delete=models.CASCADE)
    rating = models.IntegerField()

    def save(self, **kwargs):
        seller = self.rated_on.seller
        seller.n_ratings += 1
        seller.total_ratings += int(self.rating)
        seller.rating = seller.total_ratings / seller.n_ratings
        seller.save()
        super().save(**kwargs)


class Bid(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    current_highest = models.FloatField(null=True, blank=True)
    current_bidder = models.ForeignKey(BuyerProfile, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    task_id = models.CharField(max_length=200, null=True)
