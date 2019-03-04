from django.shortcuts import render
from django.http import HttpResponse
from .models import SellerProfile, BuyerProfile, User, Bid, Item, Rating
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


def index(request):
    return HttpResponse('Hello')


class GetSellerDetails(APIView):
    def get(self, request):
        seller_id = request.GET.get("sellerId")
        print(seller_id)
        seller = User.objects.get(id=seller_id)
        seller_detail = SellerProfile.objects.get(user=seller)
        if seller_detail == dict():
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data=seller_detail, status=status.HTTP_200_OK)

class PlaceBid(APIView):
    def post(self, request):
        buyer_id = request.data['buyerId']
        item_id = request.data['itemId']
        price = request.data['price']
        item = Item.objects.get(id = item_id)
        highest_bid = Bid.objects.get(item=item)
        if highest_bid['current_highest'] > price:
            return Response(data="Price lower than the highest bid", status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            Bid(item=item,current_highest= price,current_bidder= BuyerProfile.objects.get(user=User.objects.get(id=buyer_id))).save()
            return Response(status=status.HTTP_200_OK)

class RateItem(APIView):
    def post(self, request):
        item_id = request.data['ItemId']
        rating = request.data['rating']
        Rating(rated_on=Item.objects.get(id=item_id), rating=rating)
        return Response(status=status.HTTP_200_OK)
