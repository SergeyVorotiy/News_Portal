from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .forms import UserAccountForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group

class UserAccountUpdate(LoginRequiredMixin, UpdateView):
    form_class = UserAccountForm
    model = User
    template_name = 'edit.html'
    success_url = reverse_lazy('post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='author').exists()

        return context


@login_required
def authorise_me(request):
    user = request.user
    author_group = Group.objects.get(name='author')
    if not request.user.groups.filter(name='author').exists():
        author_group.user_set.add(user)
    return redirect('/news')