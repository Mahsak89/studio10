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


class BookingSubmitView(View):
    template_name = "bookingSubmit.html"

    def get(self, request):
        user = request.user
        times = [
            "3 PM", "4 PM", "5 PM"
        ]
        today = datetime.now()
        min_date = today.strftime('%Y-%m-%d')
        max_date = (today + timedelta(days=21)).strftime('%Y-%m-%d')

        day = request.session.get('day')
        service = request.session.get('service')
        hour = self.checkTime(times, day)

        return render(request, self.template_name, {
            'times': hour,
        })

    def post(self, request):
        user = request.user
        times = [
            "3 PM", "4 PM", "5 PM"
        ]
        today = datetime.now()
        min_date = today.strftime('%Y-%m-%d')
        max_date = (today + timedelta(days=21)).strftime('%Y-%m-%d')

        day = request.session.get('day')
        service = request.session.get('service')
        hour = self.checkTime(times, day)

        if not service:
            messages.success(request, "Please Select A Service!")
            return redirect('bookingSubmit')
        elif day < min_date or day > max_date:
            messages.success(
                request, "The Selected Date Isn't In The Correct Time Period!")
            return redirect('bookingSubmit')

        date = self.dayToWeekday(day)
        if date not in ['Monday', 'Saturday', 'Wednesday']:
            messages.success(request, "The Selected Date Is Incorrect")
            return redirect('bookingSubmit')

        if Appointment.objects.filter(day=day).count() >= 11:
            messages.success(request, "The Selected Day Is Full!")
            return redirect('bookingSubmit')

        time = request.POST.get("time")
        appointment_exists = Appointment.objects.filter(
            day=day, time=time).exists()
        if not appointment_exists or (appointment_exists and time == Appointment.objects.get(day=day).time):
            Appointment.objects.create(
                user=user, service=service, day=day, time=time)
            messages.success(request, "Appointment Saved!")
            return redirect('index')
        else:
            messages.success(
                request, "The Selected Time Has Been Reserved Before!")
            return redirect('bookingSubmit')

    def checkTime(self, times, day):
        # Only show the time of the day that has not been selected before:
        x = []
        for k in times:
            if Appointment.objects.filter(day=day, time=k).count() < 1:
                x.append(k)
        return x

    def dayToWeekday(self, x):
        z = datetime.strptime(x, "%Y-%m-%d")
        y = z.strftime('%A')
        return y


class UserPanelView(ListView):
    template_name = "userPanel.html"
    model = Appointment
    context_object_name = 'appointments'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).order_by('day', 'time')
