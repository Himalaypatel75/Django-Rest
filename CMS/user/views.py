from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .serializer import CreatePasswordSerializer, UserSignUpSerializer
from .models import User
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (CreateAPIView)
from django.contrib.auth import get_user_model, authenticate

# Author - Himalay Patel (02-05-2023)


User = get_user_model()

def reset_password(* _, **data):
    if User.objects.filter(email__iexact=data["email"].lower()).exists():
        user = User.objects.get(email__iexact=data["email"].lower())
        if user:
            if not default_token_generator.check_token(user, data["token"]):
                return False
            user.set_password(data["password"])
            user.save()
            return True
    else:
        return False
    
class UserSignUp(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer

    def create(self, request, *args, **kwargs):
        
        request.data['email'] = str(request.data.get('email')).lower()
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        user = User.objects.get(email = serializer.data['email'].lower())
        data =  serializer.data
        data['token'] = default_token_generator.make_token(user)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)



class CreatePasswordAPIView(CreateAPIView):
    serializer_class = CreatePasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = CreatePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                if not reset_password(**serializer.validated_data):
                    return Response(status=status.HTTP_400_BAD_REQUEST, data="invalid credentials")
                return Response({"message": "your password has been create successful", "status_code": 200})
            except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST, data="invalid credentials")
