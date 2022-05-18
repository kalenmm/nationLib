from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as LibraryAdmin
from .models import *


class UserAdmin(LibraryAdmin):
    pass


admin.site.register(Book, Comments)
admin.site.register(User, UserAdmin)
admin.site.register(Paper, Genre)
admin.site.register(Bookmarks, Author)
admin.site.register(LastPage, BugReport)
admin.site.register(Rating, GenreList)
admin.site.register(AB, ADS)
