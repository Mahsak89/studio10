from django.urls import path
from .views import IndexView, BookingView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('booking/', BookingView.as_view(), name='booking'),
]
