from django.urls import path
from .views import *

app_name = 'library'
urlpatterns = [
    path('', IndexView, name='index'),
    path('login/', LoginView, name='login'),
    path('register/', RegisterView, name='register'),
]
