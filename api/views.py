from django.http import HttpResponse
from django.utils import timezone
from django.conf import settings
from . models import SellerProfile, BuyerProfile, User, Bid, Item, Rating
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Item, Category, BuyerProfile, SellerProfile
from django.contrib.auth.models import User
from rest_framework import status
from farmbid import celery_app
from .tasks import check_for_bid_confirmation
from datetime import timedelta
import requests


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
        seller_name = request.GET.get("sellerName")
        # print(seller_id)
        try:
            seller = User.objects.get(username = seller_name)
            seller_detail = SellerProfile.objects.get(user=seller)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        obj = {
            "seller_name": seller_name,
            "Seller_rating":seller_detail.rating
        }
        if seller_detail == dict():
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(data=obj, status=status.HTTP_200_OK)


class PlaceBid(APIView):
    def post(self, request):
        buyer_id = request.data['buyerId']
        item_id = request.data['itemId']
        price = request.data['price']
        item = Item.objects.get(id=item_id)
        bid = Bid.objects.filter(item=item)
        if not bid:
            bid = Bid.objects.create(item=item, current_highest=price,
                current_bidder=BuyerProfile.objects.get(
                user=User.objects.get(id=buyer_id)))
            # schedule task
            res = check_for_bid_confirmation.apply_async(
                (bid.id,), countdown=60
            )
            bid.task_id = res.id
            bid.save()
            data = {
                'message': 'Bid placed for new item'
            }
            requests.post(settings.WEBSOCKET_URL + '/bid-placed/',
                          data=data)
            return Response({})
        bid = bid[0]
        if timezone.now() > bid.time + timedelta(seconds=60):
            return Response({'success': False,
                             'error': 'Bid time expired'})
        if bid.current_highest > price:
            return Response(data="Price lower than the highest bid",
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        bid.current_highest = price
        bid.current_bidder = buyer_id
        bid.time = timezone.now()
        bid.save()
        # delete earlier task
        celery_app.control.revoke(bid.task_id)
        # schedule task
        res = check_for_bid_confirmation.apply_async(
                (bid.id,), countdown=60
        )
        bid.task_id = res.id
        bid.save()
        requests.post(settings.WEBSOCKET_URL + '/bid-placed/',
                      data={'message': 'New bid placed'})
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
        print(request.data)
        cat = Category.objects.get(name=request.data['itemCatName'])
        print(cat)
        item = Item.objects.create(
            name=request.data['itemname'],
            seller=request.data['sellerId'],
            base_price=request.data['itemBasePrice'],
            category=cat
        )
        return Response(data={'item_id': item.id})


class ItemStats(APIView):
    def post(self, request):
        item_name = request.data['item_name']
        items = Item.objects.filter(name=item_name,
                                    cost_sold__ne=None).order_by(
            '-time'
        )
        prices = []
        cur_date = items[0].time.date
        count = 1
        sum = items[0].cost_sold
        for item in items[1:]:
            if item.time.date == cur_date:
                count += 1
                sum += item.cost_sold
            else:
                prices.append(sum / count)
                count = 1
                sum = item.cost_sold
        prices.append(sum / count)
        return Response(data=prices)



