from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),

    path('', include('catalog.urls')),
]

# Add admin panel
if settings.DEBUG:
    urlpatterns += [
        path('admin/', admin.site.urls),
    ]

# Add static files
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
