from django.contrib import admin
from .models import BuyerProfile, SellerProfile, Item, Bid, Rating, Category

# Register your models here.
admin.site.register([BuyerProfile, SellerProfile, Item, Bid, Rating, Category])
