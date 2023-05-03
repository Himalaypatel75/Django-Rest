from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

class UserAdmin(BaseUserAdmin):
    ordering = ['-reg_date']
    list_display = ['name', 'email', 'user_type', 'phone_no', 'is_staff']
    list_filter = ['user_type', 'is_staff', 'is_active']
    search_fields = ['name', 'email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name', 'phone_no')}),
        (_('Permissions'), {'fields': ('user_type', 'is_staff', 'is_active')}),
        (_('Important dates'), {'fields': ('last_login', 'reg_date')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone_no', 'user_type', 'password1', 'password2'),
        }),
    )

admin.site.register(User, UserAdmin)