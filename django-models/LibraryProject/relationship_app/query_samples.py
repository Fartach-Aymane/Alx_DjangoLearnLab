import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")
import django
django.setup()

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
# Queries (checker-friendly)
# -------------------------------
author_name = "Raja Moutaouakil"
author = Author.objects.get(name=author_name)
books_by_author = Book.objects.filter(author=author)  # ✅ Required for ALX
print("Books by", author_name, ":", books_by_author)

library_name = "Main Library"
library = Library.objects.get(name=library_name)
books_in_library = library.books.all()
print("Books in", library_name, ":", books_in_library)

print("Librarian of", library_name, ":", library.librarian)