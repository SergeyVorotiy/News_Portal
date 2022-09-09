from django.urls import path
from .views import (
   NewsList, NewsView, SearchNews, PostUpdateView, PostDelete, PostCreateView, SubscribeMe, LimiterMessage
)
from django.views.decorators.cache import cache_page

urlpatterns = [

   path('', cache_page(60)(NewsList.as_view()), name='post_list'),
   path('search', SearchNews.as_view()),
   path('<int:pk>', cache_page(60*5)(NewsView.as_view()), name='post'),
   path('<int:pk>/update/', PostUpdateView.as_view(), name='change_post'),
   path('create/', PostCreateView.as_view()),
   path('<int:pk>/delete', PostDelete.as_view()),
   path('<int:pk>/subscribe/', SubscribeMe, name='subscribe'),
   path('/limiterMessage/', LimiterMessage.as_view(), name='limiterMessage'),
]