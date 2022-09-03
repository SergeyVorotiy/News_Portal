from django.urls import path
from .views import UserAccountUpdate, authorise_me

urlpatterns = [

   path('accounts/<int:pk>/', UserAccountUpdate.as_view(), name='Account'),
   path('accounts/authorises', authorise_me, name = 'make_author'),
]