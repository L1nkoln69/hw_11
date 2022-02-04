from django.db.models import Avg, Count
from django.http import HttpResponse
from django.db.models.functions import Round  # noqa I100
from django.shortcuts import render, get_object_or_404  # noqa I101
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .mixins import *

from .models import Author, Book, Publisher, Store


def sample_view(request):
    html = '<body><h1>Django sample_view</h1><br><p>Отладка sample_view</p></body>'
    return HttpResponse(html)


def models(request, models):
    num_books = Book.objects.all()
    num_store = Store.objects.all().prefetch_related('books').annotate(books_count=Count('books'))

    num_publisher = Publisher.objects.all().prefetch_related('book_set').annotate(books_count=Count('book'))

    num_author = Author.objects.all().prefetch_related('book_set').annotate(books_count=Count('book'))

    model = {
        'book': render(request, 'book.html', context={'num_books': num_books}, ),
        'author': render(request, 'author.html', context={'num_author': num_author}, ),
        'store': render(request, 'store.html', context={'num_store': num_store}, ),
        'publisher': render(request, 'publisher.html', context={'num_publisher': num_publisher}, )
    }
    new_response = model.get(models)
    if new_response:
        return new_response
    else:
        return HttpResponse(f'такое не обслуживаем {models}')


def models_id(request, models, pk):
    num_books = get_object_or_404(Book, pk=pk)
    num_store = get_object_or_404(Store.objects.all().prefetch_related('books'), pk=pk)
    num_publisher = get_object_or_404(Publisher.objects.all().prefetch_related
                                      ('book_set').annotate(books_count=Count('book')), pk=pk)
    num_author = get_object_or_404(Author.objects.prefetch_related('book_set')
                                   .annotate(average_rating=Round(Avg('book__rating'))), pk=pk)

    model = {
        'book': render(request, 'book_id.html', context={'num_books': num_books}),
        'author': render(request, 'author_id.html', context={'num_author': num_author}),
        'store': render(request, 'store_id.html', context={'num_store': num_store}),
        'publisher': render(request, 'publisher_id.html', context={'num_publisher': num_publisher})
    }
    new_response = model.get(models)
    if new_response:
        return new_response
    else:
        return HttpResponse(f'такое не обслуживаем {models}')


class AddAuthor(LoginRequiredMixin, SuccessMessageMixin, AllFormObjects, CreateView):
    success_message = 'Author successfully created'
    login_url = '/admin/'


class SeeAuthor(SeeObjects, ListView):
    model = Author
    template_name = 'author.html'
    context_object_name = 'num_author'

    def get_queryset(self):
        return Author.objects.all().prefetch_related('book_set').annotate(books_count=Count('book'))


class OneAuthor(DetailView):
    model = Author
    template_name = 'author_id.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'num_author'

    def get_queryset(self):
        return Author.objects.prefetch_related('book_set').annotate(average_rating=Round(Avg('book__rating')))


class SeeBooks(SeeObjects, ListView):
    template_name = 'book.html'
    model = Book
    context_object_name = 'num_books'

    def get_queryset(self):
        return Book.objects.all()


class OneBook(DetailView):
    model = Book
    template_name = 'book_id.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'num_books'


class UpdateAuthor(LoginRequiredMixin, SuccessMessageMixin, AllFormObjects, UpdateView):
    pk_url_kwarg = 'pk'
    success_message = 'Author successfully updated'
    login_url = '/admin/'


class DeleteAuthor(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Author
    template_name = 'delete_author.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('see_author')
    success_message = 'Author successfully deleted'
    login_url = '/admin/'
