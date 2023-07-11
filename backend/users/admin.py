from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


@register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name')
    search_fields = ('email', 'username', 'first_name', 'last_name')
