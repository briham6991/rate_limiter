from django.urls import path
from core import views

urlpatterns = [
    path('keys/', views.CreateAPIKeyView.as_view(), name="APIkey"),


]
