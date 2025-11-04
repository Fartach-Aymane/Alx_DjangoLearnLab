from django.shortcuts import render
from .models import Book, Library

# Function-Based View: list all books
def list_books(request):
    books = Book.objects.all()

from django.views.generic import DetailView
from .models import Library

# Class-Based View: display details of a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'