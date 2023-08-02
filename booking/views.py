from django.views.generic import TemplateView, View, ListView, UpdateView
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from .models import Appointment
from django.contrib import messages
from django.urls import reverse_lazy


class IndexView(TemplateView):
    template_name = "index.html"
