from django.db.models import Avg, Count
from django.shortcuts import render, get_object_or_404
from django.db.models.functions import Round
from django.http import HttpResponse
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
        'book': render(request, 'index.html', context={'num_books': num_books}, ),
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
        'book': render(request, 'book_id.html', context={'num_books': num_books}, ),
        'author': render(request, 'author_id.html', context={'num_author': num_author}, ),
        'store': render(request, 'store_id.html', context={'num_store': num_store}, ),
        'publisher': render(request, 'publisher_id.html', context={'num_publisher': num_publisher}, )
    }
    new_response = model.get(models)
    if new_response:
        return new_response
    else:
        return HttpResponse(f'такое не обслуживаем {models}')
