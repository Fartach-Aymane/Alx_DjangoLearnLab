from django.contrib import admin
from .models import Book

# Customize the admin display
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # columns in list view
    search_fields = ('title', 'author')                     # search box
    list_filter = ('publication_year',)                     # filter by publication year

# Register the Book model with the custom admin
admin.site.register(Book, BookAdmin)