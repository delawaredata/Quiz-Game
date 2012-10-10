from django.db import models
from image_cropping.fields import ImageRatioField, ImageCropField


def uploadQuizzoPhoto(instance, filename):
    """
    Returns a directory structure like so:
    ../quizzo_photos/<filename>
    """
    return 'quizzo_photos/%s' % (filename)


class Quiz(models.Model):
    """
     Master Model which holds all the components. Quiz classes store
     publishing information, basic details and relationships with
     question objects.
    """
    headline = models.CharField('Headline', max_length=255)
    blurb = models.TextField('Quiz Description', null=True, blank=True)
    published = models.BooleanField('Published')
    pub_date = models.DateTimeField('Publish Date/Time')
    questions = models.ManyToManyField('Question', null=True, blank=True)
    quiz_photo = ImageCropField('Art', upload_to=uploadQuizzoPhoto, null=True, blank=True)
    cropping = ImageRatioField('quiz_photo', '300x400')
    slug = models.SlugField('Slug')

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = 'Quizzes'
        get_latest_by = 'pub_date'

    def is_published(self):
        return self.published

    def __unicode__(self):
        return self.headline

    def get_absolute_url(self):
        if self.published == True:
            return "/webapps/quiz/%s/%s" % (str(self.id), self.slug)


class Question(models.Model):
    """
        Basic building block for a question.
    """
    question = models.TextField('Question')
    order = models.IntegerField('Ordering', max_length=4, default=5)

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return self.question


class Answer(models.Model):
    """
        Answer model is tied to the Question model and
        also stores the number of guesses each answer
        has received. Because of this, it's important not
        to use the same answer for multiple quizzes.
    """
    question = models.ForeignKey('Question')
    answer = models.TextField('Answer', null=True, blank=True)
    order = models.IntegerField('Ordering', max_length=4, default=5)
    correct = models.BooleanField('Correct answer')
    guesses = models.IntegerField('No. of guesses', default=0)

    class Meta:
        ordering = ['order']

    def is_correct(self):
        return self.correct

    def __unicode__(self):
        return self.answer
