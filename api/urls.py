from django.urls import path
from . import views

urlpatterns = [
    path('register', views.RegisterUser.as_view()),
    path('login', views.LoginUser.as_view()),
    path('seller_details', views.GetSellerDetails.as_view()),
    path('place_bid', views.PlaceBid.as_view()),
    path('rate_item', views.RateItem.as_view()),
    path('item', views.ItemView.as_view()),
    path('item-stats', views.ItemStats.as_view()),
    path('get_uid', views.GetUserId.as_view()),
    path('', views.index),
]