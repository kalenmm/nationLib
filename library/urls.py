from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', IndexView, name='index'),
    path('login/', LoginView, name='login'),
    path('register/', RegisterView, name='register'),
    path('search/', search, name='search'),
    path('search/<str:search_type>/<str:text>', search_success, name='search_success'),
    path('book/<int:ids>/', book_page, name='book_page'),
]
