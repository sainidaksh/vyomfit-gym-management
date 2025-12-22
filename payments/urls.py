from django.urls import path
from . import views

urlpatterns = [
    path('', views.payment_list, name='payment_list'),
    path('add/<int:subscription_id>/', views.payment_add, name='payment_add'),
]

