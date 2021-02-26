from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatechars
from .models import Post


class LatestPostFeed(Feed):
    title = 'My Blog'
    linl = '/blog/'
    description = 'New post of my blog'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatechars(item.body, 30)
