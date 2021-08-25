from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from .models import Post
from django.urls import reverse

class LatestPostsFeed(Feed):
    title = "Kaye's Notes"
    link = ""
    description = "Latest Notes from Kaye"

    def items(self):
        return Post.objects.filter(status=1)

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.content, 30)

from django.utils.feedgenerator import Atom1Feed

class AtomSiteNewsFeed(LatestPostsFeed):
    feed_type = Atom1Feed
    subtitle = LatestPostsFeed.description