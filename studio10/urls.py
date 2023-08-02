from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("booking.urls")),  # Added
    path('user/', include("django.contrib.auth.urls")),
    path('user/', include("members.urls")),
]
