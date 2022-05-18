from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


class LibraryUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'id', 'authority'
    )


admin.site.register(Book)
admin.site.register(LibraryUser, LibraryUserAdmin)
admin.site.register(Paper)
admin.site.register(Genre)
admin.site.register(GenreList)
admin.site.register(Comments)
admin.site.register(Rating)
admin.site.register(Bookmarks)
admin.site.register(Author)
admin.site.register(AB)
admin.site.register(LastPage)
admin.site.register(BugReport)
admin.site.register(ADS)
