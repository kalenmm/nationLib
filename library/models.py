from django.db import models


class Book(models.Model):
    ISBN = models.IntegerField(primary_key=True)
    book_img = models.ImageField(upload_to='book_img', null=True)
    publishing_house = models.CharField(max_length=200, null=True)
    book_country = models.CharField(max_length=200, null=True)
    book_description = models.CharField(max_length=1000, null=True)
    name = models.CharField(max_length=200)
    year = models.DateTimeField('Date published')


class BookPDF(models.Model):
    id = models.AutoField(primary_key=True)
    book_content = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_pdf = models.FileField(upload_to='book_pdf')


class User(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(primary_key=False)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    first_name = models.CharField(max_length=180)
    last_name = models.CharField(max_length=180)
    authority = models.CharField(max_length=100)


class Paper(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=2200)
    paper_count = models.IntegerField()
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE)


class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)


class GenreList(models.Model):
    id = models.AutoField(primary_key=True)
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)


class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)


class Rating(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE)
    mark = models.IntegerField()


class Bookmarks(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE)
    type = models.CharField(max_length=100)


class Author(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    date_of_birth = models.DateTimeField('Date of birth')


class AB(models.Model):
    id = models.AutoField(primary_key=True)
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)


class LastPage(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    paper_id = models.ForeignKey(Paper, on_delete=models.CASCADE)


class BugReport(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    error_type = models.CharField(max_length=100)
    error_status = models.CharField(max_length=30)
    text = models.CharField(max_length=500)


class ADS(models.Model):
    id = models.AutoField(primary_key=True)
    ads = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=750)
    date_pub = models.DateTimeField('Date published')