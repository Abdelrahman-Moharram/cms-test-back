from django.contrib import admin
from django.urls import path , include
from project import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/',include('accounts.urls', namespace='accounts')),
    path('api/roles/',include('roles.urls', namespace='roles')),
    path('api/',include('djoser.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)