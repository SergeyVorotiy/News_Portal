from django.urls import path
from .views import (
   NewsList, NewsView, SearchNews, PostUpdateView, PostDelete, PostCreateView, SubscribeMe
)


urlpatterns = [

   path('', NewsList.as_view(), name='post_list'),
   path('search', SearchNews.as_view()),
   path('<int:pk>', NewsView.as_view(), name='post'),
   path('<int:pk>/update/', PostUpdateView.as_view(), name='change_post'),
   path('create/', PostCreateView.as_view()),
   path('<int:pk>/delete', PostDelete.as_view()),
   path('<int:pk>/subscribe/', SubscribeMe, name='subscribe')
]