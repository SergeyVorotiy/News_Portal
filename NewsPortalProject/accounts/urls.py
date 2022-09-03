from django.urls import path
from .views import UserAccountUpdate

urlpatterns = [

   path('accounts/<int:pk>/', UserAccountUpdate.as_view(), name='Account'),

]