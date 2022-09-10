import datetime
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_init, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import PostCategory, Post, Subscribers, PostLogDB
from .tasks import new_post_notify


@receiver(post_init, sender=PostCategory)
def category_notify_receiver(sender, instance, **kwargs):
    on_off = True

        # new_post_notify.delay()
        # recipients = []
        # for sub in Subscribers.objects.filter(category=instance.category):
        #     recipients.append(sub.user)
        # for i in recipients:
        #     html_content = render_to_string(
        #         'subMail_created.html',
        #         {
        #             'subMail': post,
        #             'recipient': i,
        #             'link_id': post.id,
        #         }
        #     )
        #
        #     msg = EmailMultiAlternatives(
        #         subject=f'{post.heading} {post.date.strftime("%Y-%m-%d")}',
        #         body=f'{post.text}',
        #         from_email='svobeckend@inbox.ru',
        #         to=[i.email],
        #     )
        #
        #     msg.attach_alternative(html_content, "text/html")
        #     msg.send()

@receiver(post_save, sender=Post)
def post_publication_log(sender, instance, created, **kwargs):
    if created:
        author = instance.author
        day = datetime.datetime.today().strftime('%d:%m:%Y')
        log_message = PostLogDB(author=author, date=day)
        log_message.save()
        print(instance.author.user.username, 'created the post', instance.heading, day)
