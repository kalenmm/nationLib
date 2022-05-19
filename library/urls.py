from django.urls import path
from . import views

app_name = 'library'
urlpatterns = [
    path('', views.IndexView, name='index'),
    path('register/', views.RegisterView, name='register'),
]
