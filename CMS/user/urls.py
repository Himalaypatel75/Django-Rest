from django.urls import path
from .views import UserSignUp, CreatePasswordAPIView, ForgotPasswordAPIView, ResetPasswordAPIView, LoginUserApi

urlpatterns = [
    path('signup/', UserSignUp.as_view(), name='user-signup'),
    path('create-password/', CreatePasswordAPIView.as_view(), name='create-password'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordAPIView.as_view(), name='reset-password'),
    path('login/', LoginUserApi.as_view(), name='login'),
    
    #we are not providing password change facility for now 😊
]