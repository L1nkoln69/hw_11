from django.core.management.base import BaseCommand

from faker import Faker

from hw_11.models import Publisher


class Command(BaseCommand):
    help = 'Creates the specified number of new publishers. You must specify a number'  # noqa: A003

    def add_arguments(self, parser):
        parser.add_argument('add_publishers', type=int, choices=range(1, 100000), help='The passed value of the '
                                                                                       'created publishers')

    def handle(self, *args, **options):
        for _ in range(options['add_publishers']):
            Publisher.objects.create(name=f'{Faker().name()} Publishing House')
            self.stdout.write(self.style.SUCCESS('Successfully added publisher "%s"' % Publisher.objects.last().name))
