from django.urls import path
from core import views

urlpatterns = [
    path('key/', views.CreateAPIKeyView.as_view(), name="APIkey"),


]
