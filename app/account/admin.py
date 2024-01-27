from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from account.models import *
# from django.utils.safestring import mark_safe
# from django.urls import reverse

# Register your models here.


User = get_user_model()

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'id', 'name', 'surname', 'is_active', 'is_superuser',)
    list_filter = ('is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('name', 'surname', 'email', )}),
        ('Profile Informations', {'fields': ('profil_image', )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_customer',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','name','surname', 'password1', 'password2')}
        ),
    )
    readonly_fields = ('timestamp',)
    search_fields = ('email', 'name', 'surname',)
    ordering = ('email',)
    filter_horizontal = ()
   


admin.site.register(User, UserAdmin)