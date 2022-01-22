
import os
import random

from django.core.management.base import BaseCommand

from faker import Faker

from hw_11.models import Book, Store


def get_books():
    books = []
    if Book.objects.all().count() < 15:
        BaseCommand().stdout.write(BaseCommand().style.ERROR('Empty/small Book sampling in db'))
        BaseCommand().stdout.write(BaseCommand().style.SUCCESS(f'Creating {15 - Book.objects.all().count()} new Book '
                                                               f'objects'))
        os.system(f'python manage.py add_book {15 - Book.objects.all().count()}')
    for i in range(random.randint(1, int(Book.objects.all().count() // 1.3))):
        books.append(
            Book.objects.get(
                pk=Book.objects.all().values_list('pk', flat=True)
                [random.randint(0,
                                len(Book.objects.all().values_list(
                                    'pk',
                                    flat=True)) - 1)]))
    return set(books)


class Command(BaseCommand):
    help = 'Creates the specified number of new stores. You must specify a number'  # noqa: A003

    def add_arguments(self, parser):
        parser.add_argument('add_stores', type=int, choices=range(1, 100000), help='The passed value of the created '
                                                                                   'stores')

    def handle(self, *args, **options):
        for _ in range(options['add_stores']):
            Store.objects.create(name=f"{Faker().name()}'s Book Store")
            books = get_books()
            for book in books:
                Store.objects.last().books.add(book)
            self.stdout.write(self.style.SUCCESS(f'Successfully added store {Store.objects.last().name}'
                                                 f' ({Store.objects.last().books.count()} books)'))
