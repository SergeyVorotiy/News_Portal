from django.urls import path
from .views import (
   NewsList, NewsView, SearchNews, PostUpdateView, PostDelete, create_post
)


urlpatterns = [

   path('', NewsList.as_view(), name='post_list'),
   path('search', SearchNews.as_view()),
   path('<int:pk>', NewsView.as_view(), name='post'),
   path('<int:pk>/update/', PostUpdateView.as_view(), name='post'),
   path('create/', create_post, name='create'),
   path('<int:pk>/delete', PostDelete.as_view())
]