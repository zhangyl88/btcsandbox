from django.urls import path

from uprofile.views import *


app_name    = 'uprofile'

urlpatterns = [
    # Update username and fullname
    path('update', UpdateView.as_view(), name='update'),
    
    # Update email
    path('update/email', UpdateEmail.as_view(), name='update-email'),
    
    
]
