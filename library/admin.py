from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


class LibraryUser(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'id', 'authority'
    )

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('is_student', 'is_teacher', 'mailing_address')
        })
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('is_student', 'is_teacher', 'mailing_address')
        })
    )


admin.site.register(Book)
admin.site.register(Comments)
admin.site.register(User, LibraryUser)
admin.site.register(Paper)
admin.site.register(Genre)
admin.site.register(Bookmarks)
admin.site.register(BookPDF)
admin.site.register(Author)
admin.site.register(LastPage)
admin.site.register(BugReport)
admin.site.register(Rating)
admin.site.register(GenreList)
admin.site.register(AB)
admin.site.register(ADS)
