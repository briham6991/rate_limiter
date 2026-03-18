from django.urls import path
from core import views

urlpatterns = [
    path('key/', views.CreateAPIKeyView.as_view(), name="APIkey"),
    path('key/<int:pk>/', views.DeleteAPIKeyView.as_view(), name="delete_api_key"),
    path('access-validate/', views.GetUserDetailsFromTokenView.as_view(), name="access_validation"),



]
