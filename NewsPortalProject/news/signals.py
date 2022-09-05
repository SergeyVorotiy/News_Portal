from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PostCategory, Post


@receiver(post_save, sender=Post)
def post_create_receiver(sender, instance, created, **kwargs):
    print('post_create_receiver: created')
    if created:
        print('post_create_receiver: created', instance)