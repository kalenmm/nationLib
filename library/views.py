
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from nationLib import settings
from .models import *
from .forms import *
from django.db.models import Sum, Value
from django.db.models.functions import Concat
from django.urls import reverse_lazy

def IndexView(request):
    template_name = "library/index.html"
    latest_books = Book.objects.order_by('pk')[:2][::-1]
    genres = Genre.objects.order_by('pk')
    populars = Rating.objects.annotate(sum=Sum('mark')).order_by('sum')[:2][::-1]
    authors = []
    last = []
    if request.user.is_authenticated:
        last = LastPage.objects.filter(user_id=request.user.pk).order_by('pk')
    news = ADS.objects.order_by('pk')
    for popular in populars:
        author = AB.objects.filter(ISBN=popular.ISBN.ISBN)
        authors.append(author[0].author_id)
    return render(request, template_name,
                  {"latest_books": latest_books, "genres": genres, 'check': populars, "authors": authors, "lasts": last, "news": news, 'media_url':settings.MEDIA_URL})


class registerView(CreateView):
    form_class = UserForm
    success_url = reverse_lazy('login')
    template_name = 'library/register.html'


def search(request):
    if request.method == "POST" and len(request.POST.get("search_field")) > 0:
        searching_text = request.POST.get("search_field")
        search_type = request.POST.get("type")
        return redirect("search_success", text=searching_text, search_type=search_type)
    else:
        return render(request, "library/search.html",
                      {"search_res": ""})


def search_success(request, text, search_type):
    search_res = ""
    if search_type == "by_name":
        search_res = Book.objects.filter(name__contains=text)
    if search_type == "by_author":
        books = AB.objects.annotate(full_name=Concat('author_id__first_name', Value(' '), 'author_id__last_name'),).filter(full_name__contains=text)
        search_res = []
        for book in books:
            search_res.append(book.ISBN)
    if search_type == "by_country":
        search_res = Book.objects.filter(book_country__contains=text)
    if search_type == "by_publisher":
        search_res = Book.objects.filter(publishing_house__contains=text)

    return render(request, "library/search.html",
                    {"search_res": search_res, "search_type": search_type, 'media_url':settings.MEDIA_URL})


def book_page(request, ids):
    book = Book.objects.filter(pk=ids)[0]
    author = AB.objects.filter(ISBN__pk=ids)[0]
    print(author.author_id.first_name)
    comments = Comments.objects.filter(ISBN__pk=ids).order_by('pk')
    pages = Paper.objects.filter(ISBN__pk=ids).order_by('paper_count')
    genres = GenreList.objects.filter(ISBN__pk=ids).order_by('genre_id__name')
    pdf = BookPDF.objects.filter(book_content__pk=ids)[0]
    return render(request, "library/book_page.html",
                  {"book": book, "author": author, "comments": comments, "pages": pages, "genres": genres, "pdf": pdf, 'media_url':settings.MEDIA_URL})


def add_genre(request):
    if request.method == 'POST' and len(request.POST.get("name")) > 0:
        genre = Genre(name=request.POST.get("name"))
        genre.save()
    return redirect("index")


def delete_genre(request):
    if request.method == 'POST' and request.user.is_staff:
        Genre.objects.filter(pk=request.POST.get("id")).delete()
    return redirect("index")


def crete_news(request):
    if request.method == 'POST' and request.user.is_staff:
        text = request.POST.get("news")
        user = request.user
        ADS(ads=user, title=text).save()
    return redirect("index")


def delete_new(request):
    if request.method == 'POST' and request.user.is_staff:
        ADS.objects.filter(pk=request.POST.get("id")).delete()
    return redirect("index")


def create_book(request):
    if request.method == 'POST' and request.user.is_staff:
        book = Book(name="New")
        book.save()
        book = Book.objects.order_by("pk")[:2][::-1][0]
        print(book.pk)
        print(book.name)
        return redirect("update_book", id=id)
    else:
        return redirect("index")


def redact_Book(request, ids):
    book = Book.objects.filter(pk=ids)[0]
    authors = Author.objects.order_by("pk")
    genres = GenreList.objects.filter(ISBN__pk=ids).order_by('genre_id__name')
    return render(request, "library/update_book.html",
                  {"book": book, "authors": authors, "genres": genres})


def profile(request):
    return redirect("index")
