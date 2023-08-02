from django.urls import path
from .views import IndexView, BookingView, BookingSubmitView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('booking/', BookingView.as_view(), name='booking'),
    path('booking/submit/', BookingSubmitView.as_view(), name='bookingSubmit'),

]
