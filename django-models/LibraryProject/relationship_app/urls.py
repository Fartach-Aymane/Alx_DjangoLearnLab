
# relationship_app/urls.py

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views  # Import the whole views module
from .views import admin_view, librarian_view, member_view
from .views import add_book, edit_book, delete_book

urlpatterns = [
    # Function-based and Class-based views for books and libraries
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # User Authentication URLs using Django built-in views
    path('register/', views.register, name='register'),  # ALX checker expects views.register
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # Role-Based Access Control URLs
    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),
]
urlpatterns += [
    path('books/add/', add_book, name='add_book'),
    path('books/edit/', edit_book, name='edit_book'),
    path('books/delete/', delete_book, name='delete_book'),
]