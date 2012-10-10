from django.contrib.syndication.views import Feed
from myproject.quizzo.models import Quiz


class LatestQuizFeed(Feed):
    title = "Did You Know quizzes"
    link = "/webapps/quiz/"
    description = "Latest Did You Know quizzes from The News Journal"

    def quizzes(self):
        return Quiz.objects.order('-pub_date')[:5]

    def title(self, quiz):
        return quiz.headline

    def link(self, quiz):
        return "http://data.delawareonline.com/webapps/quiz/%s/%s" % (quiz.id, quiz.slug)

    def description(self, quiz):
        return quiz.blurb
