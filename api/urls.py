from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('seller_detail'views.GetSellerDetails.as_view)
]