from django.db import models


class Book(models.Model):
    ISBN = models.IntegerField(primary_key=True)
    book_img = models.ImageField(upload_to='book_img')
    name = models.CharField(max_length=200)
    year = models.DateTimeField('Date published')


class BookPDF(models.Model):
    book_content = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_pdf = models.FileField(upload_to='book_pdf')


class User(models.Model):
    user_id = models.IntegerField(primary_key=False)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    first_name = models.CharField(max_length=180)
    last_name = models.CharField(max_length=180)
    authority = models.CharField(max_length=100)


class Paper(models.Model):
    text = models.CharField(max_length=2200)
    paper_count = models.IntegerField()
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE)


class Genre(models.Model):
    name = models.CharField(max_length=200)


class GenreList(models.Model):
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Comments(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)


class Rating(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE)
    mark = models.IntegerField()


class Bookmarks(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)


class Author(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    date_of_birth = models.DateTimeField('Date of birth')


class AB(models.Model):
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)


class LastPage(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    paper_id = models.ForeignKey(Paper, on_delete=models.CASCADE)


class BugReport(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    error_type = models.CharField(max_length=100)
    error_status = models.CharField(max_length=30)
    text = models.CharField(max_length=500)


class ADS(models.Model):
    ads = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=750)
    date_pub = models.DateTimeField('Date published')


