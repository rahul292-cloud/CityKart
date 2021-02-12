from django.urls import path
# from .views import ForgotPasswordView
from .views import Dashboard
urlpatterns = [
    # path('storebuddy/', Dashboard.as_view(), name='storebuddy'),
    path('', Dashboard.as_view(), name='storebuddy'),
]