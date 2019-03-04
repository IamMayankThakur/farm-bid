from celery import task
from .models import Bid
from django.conf import settings
import requests


@task
def check_for_bid_confirmation(bid_id):
    bid = Bid.objects.get(id=bid_id)
    item = bid.item
    item.buyer = bid.current_bidder
    item.cost_sold = bid.current_highest
    item.save()
    bid.delete()
    print('Bid confirmed')
    requests.post(settings.WEBSOCKET_URL + '/item-sold/',
                  data={'message': 'Item sold'})


@task
def websocket_server_reach_test():
    res = requests.get(settings.WEBSOCKET_URL + '/con-test/')
    print(res.text)