import os
import sys

# 1️⃣ Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 2️⃣ Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LibraryProject.settings")

# 3️⃣ Setup Django
import django
django.setup()

# 4️⃣ Import your models
from relationship_app.models import Author, Book, Library, Librarian

# -------------------------------
# Create sample data if empty
# -------------------------------
if not Author.objects.exists():
    # Author
    author = Author.objects.create(name="Raja Moutaouakil")

    # Books
    book1 = Book.objects.create(title="Learning Django", author=author)
    book2 = Book.objects.create(title="Advanced Django", author=author)

    # Library
    library = Library.objects.create(name="Main Library")
    library.books.set([book1, book2])

    # Librarian
    Librarian.objects.create(name="Sara", library=library)

# -------------------------------
# Run queries
# -------------------------------
author = Author.objects.get(name="Raja Moutaouakil")
library = Library.objects.get(name="Main Library")

print("Books by Raja Moutaouakil:", author.books.all())
print("Books in Main Library:", library.books.all())
print("Librarian of Main Library:", library.librarian)