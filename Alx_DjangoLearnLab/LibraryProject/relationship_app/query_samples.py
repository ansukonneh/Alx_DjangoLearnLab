from relationship_app.models import Author, Book, Library, Librarian

def query_all_books_by_author(author_name):
    author = Author.objects.filter(name=author_name).first()
    if author:
        return Book.objects.filter(author=author)
    return []

def list_all_books_in_library(library_name):
    library = Library.objects.filter(name=library_name).first()
    if library:
        return library.books.all()
    return []

def get_librarian_for_library(library_name):
    library = Library.objects.filter(name=library_name).first()
    if library:
        return Librarian.objects.filter(library=library).first()
    return None
