from django.contrib.auth.models import User
from django.http import HttpRequest
from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from .forms import UserAccountForm


class UserAccountUpdate(LoginRequiredMixin, UpdateView):
    form_class = UserAccountForm
    model = User
    template_name = 'edit.html'
    success_url = reverse_lazy('post_list')



