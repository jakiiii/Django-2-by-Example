from django.urls import path
from .feeds import LatestPostFeed
from .views import (
    post_list,
    post_detail,
    post_share,
    post_search,
)

urlpatterns = [
    path('', post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', post_detail, name='post_detail'),
    path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
    path('<int:post_id>/share/', post_share, name='post_share'),
    path('feed/', LatestPostFeed(), name='post_feed'),
    path('search/', post_search, name='post_search')
]
