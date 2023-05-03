from rest_framework import serializers
from .models import User
from rest_framework.serializers import (Serializer, EmailField, CharField, ValidationError, ModelSerializer, SerializerMethodField)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        exclude = ['is_staff', 'is_active']
        

class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['name', 'email', 'phone_no']
        

class CreatePasswordSerializer(Serializer):
    email = EmailField(label='Email Address', required=True, allow_blank=False)
    password = CharField(write_only=True, required=True, label="password")
    confirm_password = CharField(write_only=True, required=True, label="confirm_password")
    token = CharField(required=True)
