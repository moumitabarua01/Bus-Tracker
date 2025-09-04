from django.urls import path
from . import views

urlpatterns = [
    path('api/location/', views.update_location, name='update_location'),
    path('api/get-latest-location/', views.get_latest_location, name='get_latest_location'),
    path('map/', views.live_map, name='live_map'),
]
