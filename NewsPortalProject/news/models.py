import datetime

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.cache import cache
from django.utils.translation import gettext as _

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text=_('user id'))
    rating = models.IntegerField(default=0, help_text=_('author rating'))

    def update_rating(self):
        post_ratings = Post.objects.filter(author__user = self.user).values("rating")
        rating = 0
        for pr in post_ratings:
            rating += pr["rating"]*3
        com_ratings = Comment.objects.filter(post__author__user = self.user).values("rating")
        for cr in com_ratings:
            rating += cr["rating"]
        com_in_art = Comment.objects.filter(user = self.user).values("rating")
        for ciar in com_in_art:
            rating += ciar["rating"]

        self.rating = rating
        self.save()

    def __str__(self):
        return f'{self.user.username}'

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text=_('category name'))

    def __str__(self):
        return self.name

article = 'A'
news = 'N'
TYPES = [
    (news, 'Новость'),
    (article, 'Статья')
]


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, help_text=_('author id'))
    position = models.CharField(max_length=1, choices=TYPES, help_text=_('news or article'))
    date = models.DateTimeField(auto_now_add=True, help_text=_('auto date'))
    categories = models.ManyToManyField('Category', through='PostCategory', help_text=_('categories list'))
    heading = models.CharField(max_length=255, help_text=_('heading'))
    text = models.TextField(help_text=_('text'))
    rating = models.IntegerField(default=0, help_text=_('post rating'))

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f"{self.text[:124]}..."

    def __str__(self):
        return f'{self.heading}/n{self.preview()}/n{self.author}/n{self.categories.all()}'

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'product-{self.pk}')



class PostCategory(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, help_text=_('category id'))
    post = models.ForeignKey('Post', on_delete=models.CASCADE, help_text=_('post id'))

    def __str__(self):
        return f'{self.category.name}, {self.post.author.user.username}'


class Subscribers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text=_('user id'))
    category = models.ForeignKey('Category', on_delete=models.CASCADE, help_text=_('category id'))

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, help_text=_('post id'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text=_('user id'))
    text = models.TextField(help_text=_('text'))
    date = models.DateTimeField(auto_now_add=True, help_text=_('auto date'))
    rating = models.IntegerField(default=0, help_text=_('comment rating'))

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

class PostLogDB(models.Model):
    author = models.ForeignKey('Author', on_delete=models.CASCADE, help_text=_('author id'))
    date = models.CharField(max_length=16, help_text=_('date'))

    def __str__(self):
        return f'{self.author.user.username} {self.date}'