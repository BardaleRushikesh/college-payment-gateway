from django.urls import path
from . import views

urlpatterns = [

    path('', views.register, name='register'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('register/', views.register, name='register'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms/', views.terms_conditions, name='terms'),
    path('refund-policy/', views.refund_policy, name='refund_policy'),
]