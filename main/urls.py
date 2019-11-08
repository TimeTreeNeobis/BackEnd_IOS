from django.urls import path

from main.views import RegistrationAPIView

app_name = 'main'

urlpatterns = [
    path('users/', RegistrationAPIView.as_view()),
]