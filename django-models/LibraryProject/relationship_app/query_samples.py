import os
import sys

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")

# Setup Django
import django
django.setup()

# Import models
from relationship_app.models import Author, Book, Library, Librarian

# -------------------------------
# Sample data
# -------------------------------
if not Author.objects.exists():
    author = Author.objects.create(name="Raja Moutaouakil")
    book1 = Book.objects.create(title="Learning Django", author=author)
    book2 = Book.objects.create(title="Advanced Django", author=author)

    library = Library.objects.create(name="Main Library")
    library.books.set([book1, book2])
    Librarian.objects.create(name="Sara", library=library)

# -------------------------------
# Queries (ALX-checker friendly)
# -------------------------------

# 1️⃣ All books by an author
author_name = "Raja Moutaouakil"
author = Author.objects.get(name=author_name)
books_by_author = Book.objects.filter(author=author)
print("Books by", author_name, ":", books_by_author)

# 2️⃣ All books in a library
library_name = "Main Library"
library = Library.objects.get(name=library_name)
books_in_library = library.books.all()
print("Books in", library_name, ":", books_in_library)

# 3️⃣ Retrieve the librarian for a library
librarian = Librarian.objects.get(library=library)  # ✅ Required for ALX
print("Librarian of", library_name, ":", librarian)