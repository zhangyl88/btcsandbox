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


# Custom Admin - OTPs
class OTPAdmin(admin.ModelAdmin):
    list_display            = ('user', 'code', 'is_used',)
    readonly_fields         = ('id', 'user', 'code', 'timestamp',)
    
    search_fields           = ('code', 'user__email', 'user__username', 'user__ip_address', 'user__id',)

    list_filter             = ('is_used', 'timestamp',)
    
    fieldsets               = (
        (None, {'fields': ('is_used',)}),

        ('Read-Only', {'fields': ('id', 'user', 'code', 'timestamp',)}),
    )

    add_fieldsets           = (
        (None, {'fields': ('is_used',)}),

        ('Read-Only', {'fields': ('user', 'code',)}),
    )
    

# Custom Admin - Account Preferences
class PreferenceAdmin(admin.ModelAdmin):
    list_display            = ('user', 'private',)
    readonly_fields         = ('id', 'user',)

    search_fields           = ('user__email', 'user__username', 'user__ip_address', 'user__id',)

    fieldsets               = (
        ('Indicators', {'fields': ('private', 'is_email_hidden', 'two_factor_enabled',)}),
        ('Read-Only', {'fields': ('id', 'user',)})
    )

    list_filter             = ('private', 'is_email_hidden', 'two_factor_enabled',)


# Model Registrations
admin.site.register(Account, AccountAdmin)
admin.site.register(PasswordOTP, OTPAdmin)
admin.site.register(TwoFactorOTP, OTPAdmin)
admin.site.register(Preference, PreferenceAdmin)
admin.site.register(AccountConfirmationOTP, OTPAdmin)