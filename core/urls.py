from django.contrib import admin
from django.urls import path, include

# PARA INCLUIR O CAMINHO DO ARQUIVO DE MEDIA
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('app.urls')),
    path('admin/', admin.site.urls),
]

# PARA INCLUIR O CAMINHO DO ARQUIVO DE MEDIA
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)