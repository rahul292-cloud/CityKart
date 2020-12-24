from django.urls import path
# from .views import ForgotPasswordView
from .views import Dashboard
urlpatterns = [
    path('storeBody/', Dashboard.as_view(), name='VendorDashboard'),
]