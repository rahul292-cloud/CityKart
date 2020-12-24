from django.shortcuts import render
from django.shortcuts import render, redirect
from django.views.generic import ListView, View

# Create your views here.

class Dashboard(View):
    dashboard_template = 'dashboard/index.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.dashboard_template)

