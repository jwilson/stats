from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('tools/', include('tools.urls', namespace='tools')),
    path("select2/", include("django_select2.urls")),
    path('admin/', admin.site.urls),
    path('', include('core.urls', namespace='core')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)