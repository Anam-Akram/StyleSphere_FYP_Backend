from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

from fypBackend import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('User.urls')),
    path('api/', include('product.urls')),
    path('api/chat/', include('chat.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT