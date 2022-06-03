from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank, SearchHeadline
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from nationLib import settings
from .forms import *
from django.db.models import Sum, Avg, Count
from django.urls import reverse_lazy
from PyPDF2 import PdfWriter, PdfReader
import fitz
from pprint import pprint as pp
from django.db import connection, reset_queries

def IndexView(request):
    template_name = "library/index.html"
    count = 6
    if request.user.is_staff:
        count = 5
    latest_books = Book.objects.order_by('pk')[::-1][:count]
    genres = Genre.objects.order_by('pk')
    populars = Rating.objects.annotate(sum=Sum('mark')).order_by('sum')[::-1][:6]
    news = ADS.objects.order_by('pk')[:(count - 3)][::-1]
    return render(request, template_name,
                  {"latest_books": latest_books, "genres": genres, 'check': populars, "news": news, 'media_url':settings.MEDIA_URL})


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
        search_res = Book.objects.filter(name__icontains=text)
    if search_type == "by_author":
        search_res = Book.objects.filter(author_name__icontains=text)
    if search_type == "by_country":
        search_res = Book.objects.filter(book_country__icontains=text)
    if search_type == "by_publisher":
        search_res = Book.objects.filter(publishing_house__icontains=text)
    if search_type == "by_fulltext":
        vector = SearchVector('book_text')
        query = SearchQuery(text)
        search_headline = SearchHeadline('book_text', query)
        fulltext_check = BookPDF.objects.annotate(rank=SearchRank(vector, query)).annotate(headline=search_headline).filter(rank__gte=0.001).order_by('-rank')
        search_res = fulltext_check

    return render(request, "library/search.html",
                    {"search_res": search_res, "search_type": search_type, 'media_url':settings.MEDIA_URL})


def book_page(request, ids):
    book = Book.objects.filter(pk=ids)[0]
    context = {}
    last_read = 0
    book_mark = 0
    mark = []
    usr_mark = 0
    if request.user.is_authenticated:
        last_read = LastPage.objects.filter(user_id=request.user, paper_id__ISBN=book)
        book_mark = Bookmarks.objects.filter(user_id=request.user, ISBN=book)
        mark = Rating.objects.annotate(avg=Avg('mark'), count=Count('mark')).filter(ISBN=book)
        if len(mark) > 0:
            mark = [mark[0].count, mark[0].avg]
        else:
            mark = [0, 0]
        usr_mark = Rating.objects.filter(ISBN=book, user_id=request.user)
    comments = Comments.objects.filter(ISBN__pk=ids).order_by('pk')
    pages = Paper.objects.filter(ISBN__pk=ids).order_by('paper_count')
    genres = GenreList.objects.filter(ISBN__pk=ids).order_by('genre_id__name')
    all_genres = Genre.objects.order_by("name")
    pdf = BookPDF.objects.filter(book_content__pk=ids)
    if len(pdf) > 0:
        pdf = pdf[0]
    return render(request, "library/book_page.html",
                  {"book": book, "comments": comments, "usr_mark": usr_mark, "mark": mark, "all_genres": all_genres, "pages": pages, "book_mark": book_mark, "genres": genres, "pdf": pdf, 'media_url':settings.MEDIA_URL, 'last_read': last_read})


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
        return redirect("book_page", ids=book.pk)
    else:
        return redirect("index")


def add_comment(request):
    book = Book.objects.filter(pk=request.POST.get("id"))[0]
    if request.method == 'POST' and request.user.is_authenticated:
        text = request.POST.get("add_comment")
        user = request.user
        Comments(user_id=user, ISBN=book, text=text).save()
    return redirect("book_page", ids=book.pk)


def delete_comment(request):
    book = Book.objects.filter(pk=request.POST.get("id"))[0]
    if request.method == 'POST' and request.user.is_staff:
        Comments.objects.filter(pk=request.POST.get("comment")).delete()
    return redirect("book_page", ids=book.pk)


def paper_page(request, ids):
    template_name = "library/paper.html"
    paper = Paper.objects.filter(pk=ids)[0]
    if request.user.is_authenticated:
        last_read = LastPage.objects.filter(user_id=request.user, paper_id__ISBN=paper.ISBN)
        if len(last_read) > 0:
            if last_read[0].paper_id.paper_count < paper.paper_count:
                last_read[0].paper_id = paper
                last_read[0].save()
        else:
            last_read = LastPage(user_id=request.user, paper_id=paper)
            last_read.save()
    all_paper = Paper.objects.filter(ISBN=paper.ISBN)
    prev_page = Paper.objects.filter(ISBN=paper.ISBN, paper_count=paper.paper_count - 1)
    next_page = Paper.objects.filter(ISBN=paper.ISBN, paper_count=paper.paper_count + 1)
    if len(prev_page) > 0:
        prev_page = prev_page[0]
    if len(next_page) > 0:
        next_page = next_page[0]
    return render(request, template_name,
                  {"paper": paper, "all_papers": all_paper, "prev_page": prev_page, "next_page": next_page, 'media_url':settings.MEDIA_URL})


def change_book_mark(request):
    if request.method == "POST":
        book = Book.objects.filter(pk=request.POST.get("id"))[0]
        search_type = request.POST.get("type")
        book_mark = Bookmarks.objects.filter(user_id=request.user, ISBN=book)
        if search_type == "delete":
            book_mark.delete()
        else:
            if len(book_mark) == 0:
                book_mark = Bookmarks(user_id=request.user, ISBN=book, type=search_type)
            else:
                book_mark = book_mark[0]
                book_mark.type = search_type
            book_mark.save()
        return redirect("book_page", ids=book.pk)


def genre_to_book(request):
    book = Book.objects.filter(pk=request.POST.get("id"))[0]
    if request.method == 'POST' and request.user.is_staff:
        genre = request.POST.get("genre")
        genre = Genre.objects.filter(pk=genre)[0]
        check_contain = GenreList.objects.filter(ISBN=book, genre_id=genre)
        if len(check_contain) == 0 :
            genre_list = GenreList(ISBN=book, genre_id=genre)
            genre_list.save()
    return redirect("book_page", ids=book.pk)


def delete_genre_from_book(request):
    book = Book.objects.filter(pk=request.POST.get("id"))[0]
    if request.method == 'POST' and request.user.is_staff:
        genre = GenreList.objects.filter(pk=request.POST.get("genre"))
        genre.delete()
    return redirect("book_page", ids=book.pk)


def mark_book(request):
    book = Book.objects.filter(pk=request.POST.get("id"))[0]
    if request.method == 'POST' and request.user.is_authenticated:
        mark = request.POST.get("mark")
        user = request.user
        if mark == "delete":
            Rating.objects.filter(user_id=user, ISBN=book).delete()
        else:
            raiting = Rating(user_id=user, ISBN=book, mark=int(mark))
            raiting.save()
    return redirect("book_page", ids=book.pk)


def delete_book(request):
    if request.method == 'POST' and request.user.is_authenticated:
        Book.objects.filter(pk=request.POST.get("id")).delete()
    return redirect("index")


def update_book(request):
    print(request.POST.get("id"))
    book = Book.objects.filter(pk=request.POST.get("id"))[0]
    if request.method == 'POST' and request.user.is_authenticated:
        name = request.POST.get("name")
        book_country = request.POST.get("book_country")
        book_description = request.POST.get("book_description")
        publishing_house = request.POST.get("publishing_house")
        author_name = request.POST.get("author_name")
        year = request.POST.get("year")
        book_img = request.FILES[("book_img")]
        book_pdf = request.FILES[("book_pdf")]
        divide_book(book_pdf, book)
        book.name = name
        book.book_country = book_country
        book.book_description = book_description
        book.publishing_house = publishing_house
        book.author_name = author_name
        book.author_name = author_name
        book.year = year
        book.book_img = book_img
        book.save()
        text = ''
        bookpdf = BookPDF.objects.filter(book_content=book)
        if len(bookpdf) == 0:
            BookPDF(book_pdf=book_pdf, book_content=book).save()
        else:
            bookpdf[0].book_pdf = book_pdf
            bookpdf[0].save()
        bookpdf = BookPDF.objects.filter(book_content=book).order_by("pk")[::-1][0]
        loc = "./media/" + str(bookpdf.book_pdf)
        with fitz.open(loc) as doc:
            for page in doc:
                text += page.get_text()
        bookpdf.book_text = text
        bookpdf.save()
    return redirect("book_page", ids=book.pk)


def profile(request):
    if request.user.is_authenticated:
        book_marks = Bookmarks.objects.filter(user_id=request.user)
        book = []
        for book_mark in book_marks:
            book.append(book_mark.ISBN)
        last_pages = LastPage.objects.filter(paper_id__ISBN__in=book)
        book = []
        for book_mark in book_marks:
            chech = 0
            for last_page in last_pages:
                if last_page.paper_id.ISBN == book_mark.ISBN:
                    chech = last_page
            if chech != 0:
                book.append([book_mark, chech])
            else:
                book.append([book_mark, 0])
        return render(request, "library/profile.html", {"books": book, 'media_url':settings.MEDIA_URL})
    else:
        return redirect("index")


def divide_book(file, ISBN):
    inputpdf = PdfReader(file)
    for i in range(len(inputpdf.pages)):
        output = PdfWriter()
        output.addPage(inputpdf.pages[i])
        name = file.name[0:-4]
        name = name + str(i) + '.pdf'
        with open('./media/paper_pdf/' + name, "wb") as outputStream:
            output.write(outputStream)
        f = open('./media/paper_pdf/' + name)
        papers = Paper.objects.filter(paper_count=i + 1, ISBN=ISBN)
        if len(papers) > 0:
            papers[0].content = 'paper_pdf/' + name
            papers[0].save()
        else:
            paper = Paper(content='paper_pdf/' + name, paper_count=i + 1, ISBN=ISBN)
            paper.save()

def genre_selection(request):
    if request.method == 'POST':
        genres = Genre.objects.order_by("pk")
        selected = []
        for genre in genres:
            res = request.POST.get(genre.name)
            if res is not None:
                selected.append(res)
        ch = 0
        if len(selected) == 0:
            ch = 1
            selected_genres = Genre.objects.order_by("pk")
        else:
            selected_genres = Genre.objects.filter(name__in=selected)
        books = {}
        genre_lists = GenreList.objects.filter(genre_id__in=selected_genres)
        for genre_list in genre_lists:
            if genre_list.ISBN in books:
                books[genre_list.ISBN] = books[genre_list.ISBN] + 1
            else:
                books[genre_list.ISBN] = 1
        new_books = []
        for book in books:
            if ch == 0:
                if books[book] >= len(selected_genres):
                    new_books.append(book)
            else:
                new_books.append(book)
        books = new_books
        checks =[]
        for genre in genres:
            if genre in selected_genres and ch == 0:
                checks.append([genre, "yes"])
            else:
                checks.append([genre, "no"])
        return render(request, "library/catalog.html", {"books": books, "checks": checks, 'media_url': settings.MEDIA_URL})
    else:
        return redirect("index")


def catalog(request):
    books = Book.objects.order_by("pk")
    genres = Genre.objects.order_by("pk")
    checks = []
    for genre in genres:
        checks.append([genre, "no"])
    return render(request, "library/catalog.html", {"books": books, "checks": checks, 'media_url':settings.MEDIA_URL})
