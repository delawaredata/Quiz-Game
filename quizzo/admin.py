from django.contrib import admin
from myproject.quizzo.models import Quiz, Question, Answer


class AnswerInline(admin.StackedInline):
    model = Answer
    max_num = 4


class QuestionInline(admin.StackedInline):
    model = Quiz.questions.through
    inlines = [
        AnswerInline,
    ]


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'order', 'correct', 'guesses')
    list_filter = ['correct']
    search_fields = ['headline']
    exclude = ('guesses',)
    actions = ['mark_as_correct', 'mark_as_incorrect', 'zero_out_guesses']

    def mark_as_correct(self, request, queryset):
        queryset.update(correct=True)
    mark_as_correct.short_description = "Mark as correct"

    def mark_as_incorrect(self, request, queryset):
        queryset.update(correct=False)
    mark_as_incorrect.short_description = "Mark as incorrect"

    def zero_out_guesses(self, request, queryset):
        queryset.update(guesses=0)
    zero_out_guesses.short_description = "Reset number of guesses"


class QuizAdmin(admin.ModelAdmin):
    list_display = ('headline', 'published', 'pub_date')
    list_filter = ['published', 'pub_date']
    search_fields = ['headline']
    raw_id_fields = ('questions',)
    ordering = ['-pub_date']
    prepopulated_fields = {'slug': ("headline",)}
    actions = ['mark_as_published', 'mark_as_unpublished']
    inlines = [
        QuestionInline,
    ]
    exclude = ('questions',)

    def mark_as_published(self, request, queryset):
        queryset.update(published=True)
    mark_as_published.short_description = "Publish"

    def mark_as_unpublished(self, request, queryset):
        queryset.update(published=False)
    mark_as_unpublished.short_description = "Unpublish"


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'order', 'id')
    list_editable = ('order',)
    search_fields = ['question']
    inlines = [
        AnswerInline,
    ]


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
