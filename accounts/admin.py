from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile

# Register your models here.

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_staff']
    ordering = ['email']
    fieldsets = UserAdmin.fieldsets + (
        ('Додатково', {'fields': ('phone', 'avatar')}),
    )