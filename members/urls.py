from django.urls import path
from . import views

urlpatterns = [
    path('', views.members_list, name='members_list'),
    path('add/', views.add_member, name='add_member'),
    path('edit/<int:id>/', views.member_edit, name='member_edit'),
    path('delete/<int:id>/', views.member_delete, name='member_delete'),
    path('<int:id>/', views.member_detail, name='member_detail'),
    
]
