from django.shortcuts import render
from django.http import HttpResponse
from . models import SellerProfile, BuyerProfile, User, Bid, Item, Rating
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Item, Category, BuyerProfile, SellerProfile
from django.contrib.auth.models import User
from rest_framework import status


def index(request):
    return HttpResponse('Hello')


class RegisterUser(APIView):
    def post(self, request):
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']
        if User.objects.filter(email=email).exists():
            data = {'success': False, 'error': 'Email already exists'}
            return Response(data)
        if User.objects.filter(username=username).exists():
            data = {'success': False, 'error': 'Username already exists'}
            return Response(data)
        user = User.objects.create_user(username, email=email, password=password)
        if request.data['user-kind'] == 'BUYER':
            BuyerProfile.objects.create(
                user=user
            )
        else:
            SellerProfile.objects.create(
                user=user,
                aadhar_no=request.data['aadhar_no'],
            )
        return Response(data={})


class LoginUser(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        if not User.objects.filter(email=email).exists():
            return Response({'success': False, 'error': 'Email does not exist'})
        user = User.objects.get(email=email)
        if not user.check_password(password):
            return Response({'success': False, 'error': 'Password is invalid'})
        return Response({'success': True, 'email': email,})
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
        item = Item.objects.get(id=item_id)
        highest_bid = Bid.objects.get(item=item)
        if highest_bid['current_highest'] > price:
            return Response(data="Price lower than the highest bid", status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            Bid(item=item, current_highest=price, current_bidder=BuyerProfile.objects.get(
                user=User.objects.get(id=buyer_id))).save()
            return Response(status=status.HTTP_200_OK)


class RateItem(APIView):
    def post(self, request):
        item_id = request.data['ItemId']
        rating = request.data['rating']
        Rating(rated_on=Item.objects.get(id=item_id), rating=rating)
        return Response(status=status.HTTP_200_OK)


class Item(APIView):
    def get(self, request):
        items = Item.objects.filter(cost_sold=None)
        data = []
        for item in items:
            dic = {
                'itemName': item.name,
                'itemId': item.id,
                'basePrice': item.base_price,
                'sellerId': item.seller.id,
                'sellerName': item.seller.user.username,
                'sellerRating': item.seller.rating,
            }
            data.append(dic)
        return Response(data=data)

    def post(self, request):
        cat = Category.objects.get(name=request.data['itemCatName'])
        item = Item.objects.create(
            name=request.data['itemname'],
            seller=request.data['sellerId'],
            base_price=request.data['itemBasePrice'],
            category=cat
        )
        return Response(data={'item_id': item.id})
