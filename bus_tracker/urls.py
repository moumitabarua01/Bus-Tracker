from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('bus/', include("bus.urls")),
    path('authentication/', include('authentication.urls')),
    # path('gsm/',include("gsm.urls")),
    # path('tracking/',include("tracking.urls")),
    path('', views.home, name='home'),
    path('tracker/', include('tracker.urls')),
    path('book/', include('seatBokking.urls', namespace='seatBokking')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
