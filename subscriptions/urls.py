from django.urls import path
from . import views

urlpatterns = [
    path('', views.subscriptions_list, name='subscriptions_list'),
    path('add/', views.add_subscription, name='add_subscription'),
    path('renew/<int:id>/', views.renew_subscription, name='renew_subscription'),
    path('delete/<int:id>/', views.subscription_delete, name='subscription_delete'),
    path('refresh_expiry/', views.refresh_expiry, name='refresh_expiry'),
    path('undo/', views.undo_action, name='undo_action'),   # <-- ⭐ ADD THIS
    path('payments/', views.payments_list, name='payments_list')
]
