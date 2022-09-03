from django.db import models

from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class SignupForm(SignupForm):

    def save(self, request):
        user = super(SignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user