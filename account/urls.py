from django.urls import path

from account.views import *

app_name    = "account"

###ACCOUNT
urlpatterns = [
    #! Basic Authentication
    #001 Register a new user ~ Sign up
    path('create', CreateView.as_view(), name='create'),
    
    #002 Confirm user account
    #### Needed during withdrawals
    path('confirm', ConfirmView.as_view(), name='confirm'),

    #003 Resend confirmation OTP
    path('resend-confirm', ResendConfirm.as_view(), name='resend-confirm'),
    
    #004 Authorize a user ~ Login
    path('authorize', Authorize.as_view(), name='authorize'),
    
    #! Two-Factor Authentication
    #005 Generates and sends 2-Factor Authorization Code
    path('authorize/2/generate', TwoFactorGenerator.as_view(), name='two-factor-generator'),
    
    #006 Confirm 2-Factor Authentication
    path('authorize/2/confirm', ConfirmAuthorization.as_view(), name='confirm-authorization'),
    
    #!Forgot Password
    #007 Reset account password
    path('password/reset', ResetPassword.as_view(), name='reset-password'),

    #08 Confirm account password reset code
    path('password/reset/confirm', ConfirmPasswordResetCode.as_view(), name='confirm-password-reset-code'),

    #09 Set new account password
    path('password/reset/set', SetPassword.as_view(), name='set-password'),
    
    
    #010 Check username availability
    path('av/username', CheckUsernameAv.as_view(), name='check-username-availability'),

    #011 Check email availability
    path('av/email', CheckEmailAv.as_view(), name='check-email-availability'),

    #!Forgot Email
    #012 Get email with username
    path('get/email.username', GetEmailUsername.as_view(), name='get-email_username'),
    
        
    #!Logout
    #013 Logout all devices associated with specified user account
    path('logout/all', LogoutAllAccounts.as_view(), name='logout-all-accounts'),
]