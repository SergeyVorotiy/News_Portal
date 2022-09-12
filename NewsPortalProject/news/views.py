import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from .forms import PostForm
from .models import Post, Comment, Author, Subscribers, PostLogDB, Category
from .filters import PostFilter
from .tasks import new_post_notify
from django.core.cache import cache
from django.utils.translation import gettext as _
import logging
from django.utils import timezone
import pytz


# logger_debug = logging.getLogger('console_debug')
# logger_warning = logging.getLogger('console_warning')
# logger_error_console = logging.getLogger('console_error')
# logger_general = logging.getLogger('general_log')
# logger_errors_file = logging.getLogger('errors_log')
# logger_security = logging.getLogger('security_log')


@login_required
def SubscribeMe(request, pk):
    user = request.user
    post = Post.objects.get(id=pk)
    categories = post.categories.all()
    for category in categories:
        its_ok = False
        subscribe = Subscribers(user=user, category=category)
        for s in Subscribers.objects.all():
            if subscribe.user == s.user and subscribe.category == s.category:
                its_ok = False
                break
            else:
                its_ok = True
        if its_ok:
            subscribe.save()
    url = '/news/'+str(pk)

    return HttpResponseRedirect(url)


class NewsList(ListView):
    model = Post

    ordering = '-date'

    template_name = 'articles.html'

    context_object_name = 'articles'

    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['current_time'] = timezone.now()
        return context


class SearchNews(ListView):
    model = Post

    ordering = '-date'

    template_name = 'search.html'

    context_object_name = 'search'

    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['current_time'] = timezone.now()
        return context


class CommentList(ListView):
    model = Comment

    ordering = 'date'

    template_name = 'article.html'

    context_object_name = 'comments'

class NewsView(DetailView):
    model = Post

    template_name = 'article.html'

    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        return context


class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', )
    form_class = PostForm
    model = Post
    template_name = 'edit.html'

    def form_valid(self, form):
        postQ = form.save(commit=False)
        current_user = Author.objects.get(user=self.request.user)
        if not current_user:
            current_user = current_user.objects.create(user=self.request.user)
        postQ.author = current_user
        if 'news' in str(self.request):
            postQ.position = 'N'
        else:
            postQ.position = 'A'
        day = datetime.datetime.today().strftime('%d:%m:%Y')
        today_author_log = PostLogDB.objects.filter(date=day, author=current_user)
        if today_author_log.count() <= 40:
            postQ.save()
            form.save()
            new_post_notify.delay()
            pk = postQ.id
            return HttpResponseRedirect(f'../{pk}')
        else:
            return HttpResponseRedirect(reverse_lazy('limiterMessage'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        return context


class LimiterMessage(TemplateView):
    template_name = 'limiterMessage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        return context


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post', )
    form_class = PostForm
    model = Post
    template_name = 'edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        return context


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post', )
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.now()
        return context


def chenge_time_zone(request):
    current_time = timezone.now()
    context = {
        'current_time': timezone.now(),
        'timezones': pytz.common_timezones,
    }
    if request.POST:
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/chengetime/')


    return HttpResponse(render(request, 'chenge_time_zone.html', context))


def chenge_language(request):
    context = {
        'current_time': timezone.now(),
    }
    return HttpResponse(render(request, 'chenge_language.html', context))