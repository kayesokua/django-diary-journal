from . import views
from django.urls import include
from django.conf.urls import url
from django.urls import path
from .feeds import LatestPostsFeed, AtomSiteNewsFeed

urlpatterns = [
    path("feed/rss", LatestPostsFeed(), name="post_feed"),
    path("feed/atom", AtomSiteNewsFeed()),
    path("", views.PostList.as_view(), name="home"),
    path("about", views.about_me, name="about_me"),
    url(r'^tagged/(?P<tag>[\w-]+)/$', views.tag_detail, name='tag_detail'),
    path("<slug:slug>/", views.post_detail, name="post_detail"),
    path("<slug:slug>/like", views.like_post, name="like"),
    path("<slug:slug>/unlike", views.unlike_post, name="unlike"),
    path("search", views.post_search, name="post_search")
]