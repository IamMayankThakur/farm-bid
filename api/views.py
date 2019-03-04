from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Item, Category


def index(request):
    return HttpResponse('Hello')


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
