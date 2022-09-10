from django.core.management.base import BaseCommand, CommandError
from news.models import PostCategory, Post, Category


class Command(BaseCommand):
    help = 'delete post with category from args'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('category_name', nargs='+', type=str)

    def handle(self, category_name, **options):
        # здесь можете писать любой код, который выполнется при вызове вашей команды
        self.stdout.readable()
        self.stdout.write(
            'Do you really want to delete all post in category yes/no')  # спрашиваем пользователя действительно ли он хочет удалить все товары
        answer = input()  # считываем подтверждение

        if answer == 'yes':
            deleted_category = Category.objects.get(name=str(category_name[1]))
            
            self.stdout.write(self.style.SUCCESS(f'Succesfully wiped posts! {deleted_category}'))
            return

        self.stdout.write(self.style.ERROR('Access denied'))

