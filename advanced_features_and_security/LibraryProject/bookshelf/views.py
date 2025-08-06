from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, ExampleForm
from django.contrib.auth.decorators import permission_required, login_required
from django.core.exceptions import PermissionDenied
from .models import Book
from .forms import ExampleForm

# Only one book_list view, combining both permissions and logic
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    query = request.GET.get("q")
    books = Book.objects.all()
    if query:
        books = books.filter(title__icontains=query)
    return render(request, 'bookshelf/book_list.html', {'books': books})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect_user_dashboard(user)
    else:
        form = CustomUserCreationForm()
    return render(request, 'your_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect_user_dashboard(user)
    else:
        form = AuthenticationForm()
    return render(request, 'your_app/login.html', {'form': form})

def redirect_user_dashboard(user):
    if user.role == 'librarian':
        return redirect('librarian_dashboard')
    elif user.role == 'student':
        return redirect('student_dashboard')
    else:
        return redirect('home')

@login_required
def example_form_view(request):
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = ExampleForm()

    return render(request, 'bookshelf/form_example.html', {'form': form})

def raise_exception(request):
    raise PermissionDenied("You do not have permission to view this page.")


def books(request):
    return render(request, 'bookshelf/book_list.html')