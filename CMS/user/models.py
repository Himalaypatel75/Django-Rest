from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, name, phone_no, user_type, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone_no=phone_no,
            user_type=user_type
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone_no, user_type, password):
        user = self.create_user(
            email=email,
            name=name,
            phone_no=phone_no,
            password=password,
            user_type = "Admin"
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user

user_type = [
    ('Admin', 'Admin'),
    ('Customer', 'Customer'),
]

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=150,  blank=True, null=True)
    email = models.EmailField(max_length=150, unique=True)
    phone_no = models.CharField(max_length=14,  blank=True)
    user_type = models.CharField(choices=user_type, max_length=30, default='Customer')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    reg_date = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'user_type','phone_no']

    objects = UserManager()