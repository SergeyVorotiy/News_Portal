import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
)
from .forms import PostForm
from .models import Post, Comment, Author, Subscribers, PostLogDB
from .filters import PostFilter
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives



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
        context['filteset'] = self.filterset
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
        print(today_author_log)
        if today_author_log.count() <= 3:
            postQ.save()
            form.save()
            return HttpResponseRedirect('../')
        else:
            return HttpResponseRedirect(reverse_lazy('limiterMessage'))


class LimiterMessage(TemplateView):
    template_name = 'limiterMessage.html'

class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post', )
    form_class = PostForm
    model = Post
    template_name = 'edit.html'


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post', )
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('post_list')

