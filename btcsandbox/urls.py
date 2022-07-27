from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Site URL Registration
urlpatterns = [
    # sandbox backdoor
    path('admin/', admin.site.urls),
    
    # account
    path('v1/account/', include('account.urls', namespace='account')),
]

# Developemntal Purposes [Media Directory]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)