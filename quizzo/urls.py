from django.conf.urls.defaults import *
from myproject.quizzo.feeds import LatestQuizFeed

urlpatterns = patterns('myproject.quizzo.views',  # Common Prefix

    # MAIN PAGE
    url(r'^$', 'index'),
    # QUIZ PAGE
    url(r'^(?P<quiz_id>\d+)/(?P<quiz_slug>[-\w]+)/$', 'quiz_page'),
    # RESULTS PAGE
    url(r'^(?P<quiz_id>\d+)/(?P<quiz_slug>[-\w]+)/results/$', 'quiz_results'),
    # SEARCH PAGE
    url(r'^search/$', 'search_page')

)
# URL Patterns for RSS feeds.
urlpatterns += patterns('',
    url(r'^latest/feed/$', LatestQuizFeed()),
)
