from django.urls import path
from .views import IndexView, BookingView, BookingSubmitView, UserPanelView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('booking/', BookingView.as_view(), name='booking'),
    path('booking/submit/', BookingSubmitView.as_view(), name='bookingSubmit'),
    path('user/panel/', UserPanelView.as_view(), name='userPanel'),


]
