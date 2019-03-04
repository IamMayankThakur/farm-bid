from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Item, Category, BuyerProfile, SellerProfile
from django.contrib.auth.models import User


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
