from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

admin.site.register(Book)
admin.site.register(Comments)
admin.site.register(User)
admin.site.register(Paper)
admin.site.register(Genre)
admin.site.register(Bookmarks)
admin.site.register(Author)
admin.site.register(LastPage)
admin.site.register(BugReport)
admin.site.register(Rating)
admin.site.register(GenreList)
admin.site.register(AB)
admin.site.register(ADS)
