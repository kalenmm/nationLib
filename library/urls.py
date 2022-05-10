from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    path('', views.IndexView, name='index'),
    path('login/', views.LoginView, name='login'),
    path('register/', views.RegisterView, name='register'),
]
