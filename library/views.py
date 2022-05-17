from django.shortcuts import render
# from django.views.generic import CreateView, DetailView, ListView, TemplateView
from .models import *
from django.db.models import Sum

def IndexView(request):
    template_name = "library/index.html"
    latest_books = Book.objects.order_by('pk')[:2][::-1]
    genres = Genre.objects.order_by('pk')
    populars = Rating.objects.annotate(sum=Sum('mark')).order_by('sum')[:2][::-1]
    authors = []
    last = LastPage.objects.order_by('pk')
    news = ADS.objects.order_by('pk')
    for popular in populars:
        author = AB.objects.filter(ISBN=popular.ISBN.ISBN)
        authors.append(author[0].author_id)
    return render(request, template_name,
                  {"latest_books": latest_books, "genres": genres, 'check': populars, "authors": authors, "lasts": last, "news": news})


def LoginView(request):
    template_name = "library/login.html"
    return render(request, template_name)


def RegisterView(request):
    template_name = "library/register.html"
    return render(request, template_name)