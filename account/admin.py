from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.models import *


# Custom Admin - Account
class AccountAdmin(UserAdmin):
    list_display            = ('email', 'username', 'is_confirmed', 'ip_address',)
    readonly_fields         = ('id', 'date_joined', 'last_login',)
    search_fields           = ('email', 'username', 'ip_address', 'id',)

    ordering                = [('-date_joined'),]

    filter_horizontal       = ()
    list_filter             = ('is_active', 'is_confirmed', 'date_joined',)
  
    fieldsets               = (
        ('Basic Informations', {'fields': ('email', 'username', 'fullname',)}),

        ('Security Required', {'fields': ('password',)}),

        ('Auto Generated', {'fields': ('ip_address',)}),

        ('Indicators', {'fields': ('is_admin', 'is_active', 'is_confirmed', 'is_superuser', 'is_staff',)}),
        
        ('Read-Only', {'fields': ('id', 'date_joined', 'last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'passcode', 'password1', 'password2',)
        }),
    )


# Model Registrations
admin.site.register(Account, AccountAdmin)