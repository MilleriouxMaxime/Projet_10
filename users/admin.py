from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'birth_date', 'can_be_contacted', 'can_data_be_shared', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'can_be_contacted', 'can_data_be_shared')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'birth_date')}),
        ('Privacy settings', {'fields': ('can_be_contacted', 'can_data_be_shared')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'birth_date', 'first_name', 'last_name',
                      'can_be_contacted', 'can_data_be_shared'),
        }),
    )
