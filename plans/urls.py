from django.urls import path
from . import views

urlpatterns = [
    path("", views.plans_list, name="plans_list"),
    path("create/", views.plan_create, name="plan_create"),
    path("edit/<int:id>/", views.plan_edit, name="plan_edit"),
    path("delete/<int:id>/", views.plan_delete, name="plan_delete"),
]
