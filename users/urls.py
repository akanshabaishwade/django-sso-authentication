from django.urls import path
from .views import RegisterAPIView, LoginAPIView, ContinueLoginAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('continue-login/', ContinueLoginAPIView.as_view(), name='continue-login'),
]
