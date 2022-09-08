from celery import shared_task
import time
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from news.models import Post, Subscribers, PostCategory, Category

# Отправка уведомления о новой новости подписчикам
@shared_task
def new_post_notify():
    instance = PostCategory.objects.last()
    post = Post.objects.last()
    recipients = []
    for sub in Subscribers.objects.filter(category=instance.category):
        recipients.append(sub.user)
    for user in recipients:
        html_content = render_to_string(
            'subMail_created.html',
            {
                'subMail': post,
                'recipient': user,
                'link_id': post.id,
            }
        )
        msg = EmailMultiAlternatives(
            subject=f'{post.heading} {post.date.strftime("%Y-%m-%d")}',
            body=f'{post.text}',
            from_email='svobeckend@inbox.ru',
            to=user.email,
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()

# Отправка писем с последними новостями
@shared_task
def every_week_notify():
    for category in Category.objects.all():
        recipients = []
        for sub in Subscribers.objects.filter(category=category):
            recipients.append(sub.user.email)
        filtered_posts = Post.objects.filter(categories=category)

        html_content = render_to_string(
            'subMail_in_week.html',
            {
                'subMail': filtered_posts,

            }
        )

        msg = EmailMultiAlternatives(
            subject=f'Дайджест за неделю!',
            body=f'',
            from_email='svobeckend@inbox.ru',
            to=recipients,
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()