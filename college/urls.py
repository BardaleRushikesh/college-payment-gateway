from django.urls import path
from . import views

urlpatterns = [

    path('', views.register, name='register'),
    path('payment-success/', views.payment_success, name='payment_success'),

]