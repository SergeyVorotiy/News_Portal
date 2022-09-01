import datetime

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

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
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

article = 'A'
news = 'N'
TYPES = [
    (news, 'Новость'),
    (article, 'Статья')
]


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    position = models.CharField(max_length=1, choices=TYPES)
    date = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField('Category', through='PostCategory')
    heading = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f"{self.text[:124]}..."

    def __str__(self):
        return f'{self.heading}/n{self.preview()}/n{self.author}'

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])



class PostCategory(models.Model):
    post = models.ForeignKey('Category', on_delete=models.CASCADE)
    category = models.ForeignKey('Post', on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()