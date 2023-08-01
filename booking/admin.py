from django.contrib import admin
from .models import *


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):

    list_display = ('user', 'service', 'day', 'time')
    search_fields = ['user', 'service']
    list_filter = ('service', 'day')
