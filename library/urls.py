from django.urls import path
from .views import *
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', IndexView, name='index'),
    path('login/', LoginView.as_view(template_name="library/login.html"), name="login"),
    path("register/", registerView.as_view(), name="registration"),
    path('search/', search, name='search'),
    path('search/<str:search_type>/<str:text>', search_success, name='search_success'),
    path('book/<int:ids>/', book_page, name='book_page'),
    path('paper/<int:ids>/', book_page, name='paper_page'),
    path('add_genre/', add_genre, name='add_genre'),
    path('delete_genre/', delete_genre, name='delete_genre'),
    path('crete_news/', crete_news, name='crete_news'),
    path('delete_new/', delete_new, name='delete_new'),
    path('create_book/', create_book, name='create_book'),
    path('redact_Book/<int:ids>', create_book, name='redact_Book'),
    path('profile/', profile, name='profile'),
    path('add_comment/', add_comment, name='add_comment'),
    path('delete_comment/', delete_comment, name='delete_comment'),
    path('paper_page/<int:ids>', paper_page, name='paper_page'),
    path('change_book_mark/', change_book_mark, name='change_book_mark'),
    path('genre_to_book/', genre_to_book, name='genre_to_book'),
    path('delete_genre_from_book/', delete_genre_from_book, name='delete_genre_from_book'),
    path('mark_book/', mark_book, name='mark_book'),
    path('delete_book/', delete_book, name='delete_book'),
    path('update_book/', update_book, name='update_book'),
]
