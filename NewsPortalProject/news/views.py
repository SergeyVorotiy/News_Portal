from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .forms import PostForm
from .models import Post, Comment, Author
from .filters import PostFilter
from django.contrib.auth.models import Group

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
        form.save()
        return HttpResponseRedirect('../')


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



    # def form_valid(self, form):
    #     post = form.save(commit=False)
    #     current_user = Author.objects.get(user=self.current_request.user)
    #     if not current_user:
    #         author = current_user.objects.create(user=self.current_request.user)
    #     post.author = current_user
    #     if 'news' in str(self.current_request):
    #         post.position = 'N'
    #     else:
    #         post.position = 'A'
    #     form.save()
    #     return HttpResponseRedirect('../')

@login_required
def create_post(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST)
        post = form.save(commit=False)
        current_user = Author.objects.get(user=request.user)
        author_group = Group.objects.get(name='author')
        if not current_user:
            author = current_user.objects.create(user=request.user)

        if not request.user.groups.filter(name='author').exists():
            author_group.user_set.add(current_user)

        post.author = current_user
        if 'news' in str(request):
            post.position = 'N'
        else:
            post.position = 'A'
        form.save()
        return HttpResponseRedirect('../')

    return render(request, 'edit.html', {'form':form})
