from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin for user"""
    list_display = (
        'pk',
        'username',
        'last_name',
        'first_name',
        'father_name',
        'email',
        'phone_number',
    )
    search_fields = (
        'last_name',
        'email',
        'phone_number',
    )
    ordering = ('first_name',)
