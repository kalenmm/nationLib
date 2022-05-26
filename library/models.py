from django.db import models, migrations
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.operations import TrigramExtension


class Migration(migrations.Migration):
    operations = [
        TrigramExtension(),
    ]


class Book(models.Model):
    ISBN = models.AutoField(primary_key=True)
    book_img = models.ImageField(upload_to='book_img', null=True)
    publishing_house = models.CharField(max_length=200, null=True)
    book_country = models.CharField(max_length=200, null=True)
    book_description = models.CharField(max_length=1000, null=True)
    name = models.CharField(max_length=200)
    author_name = models.CharField(max_length=200, null=True)
    year = models.DateTimeField('Date published', null=True)


class BookPDF(models.Model):
    id = models.AutoField(primary_key=True)
    book_content = models.ForeignKey(Book, on_delete=models.CASCADE)
    book_pdf = models.FileField(upload_to='book_pdf')


class User(AbstractUser):

    def __str__(self):
        return self.username

    def get_name(self):
        return self.username


class Paper(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.FileField(upload_to='paper_pdf')
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
    date_pub = models.DateTimeField(auto_now_add=True, blank=True)
