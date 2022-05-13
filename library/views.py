from django.shortcuts import render
# from django.views.generic import CreateView, DetailView, ListView, TemplateView
from .models import *
from django.db.models import Sum

def IndexView(request):
    template_name = "library/index.html"
    latest_books = Book.objects.order_by('pk')[:2][::-1]
    genres = Genre.objects.order_by('pk')
    check = Rating.objects.annotate(sum=Sum('mark')).order_by('sum')[:2][::-1]
    print(check[1].ISBN.name)
    return render(request, template_name,
                  {"latest_books": latest_books, "genres": genres, 'check' : check})


def LoginView(request):
    template_name = "library/login.html"
    return render(request, template_name)


def RegisterView(request):
    template_name = "library/register.html"
    return render(request, template_name)

