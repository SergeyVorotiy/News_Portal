import datetime
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_init, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import PostCategory, Post, Subscribers, PostLogDB


@receiver(post_init, sender=PostCategory)
def category_notify_receiver(sender, instance, **kwargs):
    on_off = True
    if on_off:
        print('post_create_receiver: created', instance)
        post = Post.objects.last()
        recipients = []
        for sub in Subscribers.objects.filter(category=instance.category):
            recipients.append(sub.user)
        for i in recipients:
            html_content = render_to_string(
                'subMail_created.html',
                {
                    'subMail': post,
                    'recipient': i,
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'{post.heading} {post.date.strftime("%Y-%m-%d")}',
                body=f'{post.text}',
                from_email='Vorotiy.Sergey@yandex.ru',
                to=[i.email],
            )

            msg.attach_alternative(html_content, "text/html")
            msg.send()

@receiver(post_save, sender=Post)
def post_publication_log(sender, instance, created, **kwargs):
    if created:
        author = instance.author
        day = datetime.datetime.today().strftime('%d:%m:%Y')
        log_message = PostLogDB(author=author, date=day)
        log_message.save()
        print(instance.author.user.username, 'created the post', instance.heading, day)
