from django.urls import path
from .views import UserSignUp, CreatePasswordAPIView


urlpatterns = [
    path('signup/', UserSignUp.as_view(), name='user-signup'),
    path('create-password/', CreatePasswordAPIView.as_view(), name='create-password'),
]