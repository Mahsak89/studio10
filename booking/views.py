from django.views.generic import TemplateView, View, ListView, UpdateView
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import Appointment
from django.contrib import messages
from django.urls import reverse_lazy


class IndexView(TemplateView):
    template_name = "index.html"


class BookingView(View):
    template_name = "booking.html"
    weekdays = []
    validate_weekdays = []

    def get(self, request):
        today = datetime.now()
        self.weekdays = self.validWeekday(22)
        self.validate_weekdays = self.isWeekdayValid(self.weekdays)
        return render(request, self.template_name, {
            'weekdays': self.weekdays,
            'validateWeekdays': self.validate_weekdays,
        })

    def post(self, request):
        service = request.POST.get('service')
        day = request.POST.get('day')
        if not service:
            messages.success(request, "Please Select A Service!")
            return redirect('booking')

        request.session['day'] = day
        request.session['service'] = service
        return redirect('bookingSubmit')

    def validWeekday(self, days):
        # Loop days you want in the next 21 days:
        today = datetime.now()
        weekdays = []
        for i in range(0, days):
            x = today + timedelta(days=i)
            y = x.strftime('%A')
            if y == 'Monday' or y == 'Saturday' or y == 'Wednesday':
                weekdays.append(x.strftime('%Y-%m-%d'))
        return weekdays

    def isWeekdayValid(self, x):
        validateWeekdays = []
        for j in x:
            if Appointment.objects.filter(day=j).count() < 10:
                validateWeekdays.append(j)
        return validateWeekdays
