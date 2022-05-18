from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as LibraryAdmin
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



class UserAdmin(LibraryAdmin):
    pass


admin.site.register(Book, Comments)
admin.site.register(User, UserAdmin)
admin.site.register(Paper, Genre)
admin.site.register(Bookmarks, Author)
admin.site.register(LastPage, BugReport)
admin.site.register(Rating, GenreList)
admin.site.register(AB, ADS)
