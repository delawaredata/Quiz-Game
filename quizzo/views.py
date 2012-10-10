from myproject.quizzo.models import *
from myproject.quizzo.forms import *
from django.db.models import Q
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from datetime import datetime


def _get_correct_answer(question):
    """
    Helper function to get the correct answer.
    And the total number of guesses.
    """
    answers = question.answer_set.all()
    num_guesses = 0
    for answer in answers:
        num_guesses += answer.guesses
        if answer.is_correct():
            correct_answer = answer
    return correct_answer, num_guesses


def _get_next_and_previous(quiz):
    """
    A helper function that grabs the next
    and previous **published** quizzes. Use this
    instead of built-in "get_FOO_by_pub_date()"
    because that doesn't consider published
    status.
    """
    # Get the previous published quiz.
    try:
        pre = quiz.get_previous_by_pub_date()
        while not (pre.is_published() and pre.pub_date <= datetime.now()):
            try:
                pre = pre.get_previous_by_pub_date()
            except:
                pre = None
                break
    except:
        pre = None

    # Get the next published quiz
    try:
        next = quiz.get_next_by_pub_date()
        while not (next.is_published() and next.pub_date <= datetime.now()):
            try:
                next = next.get_next_by_pub_date()
            except:
                next = None
                break
    except:
        next = None

    return pre, next


def index(request):
    """
    Our main page. Uses pagination and lists
    10 quizzes per page.
    """
    all_quizzes = Quiz.objects.filter(published=True, pub_date__lte=datetime.now()).order_by('-pub_date')
    pagination = True
    paginator = Paginator(all_quizzes, 10)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        quizzes = paginator.page(page)
    except (EmptyPage, InvalidPage):
        quizzes = paginator.page(paginator.num_pages)

    variables = RequestContext(request, {
        'pagination': pagination,
        'quizzes': quizzes
    })

    return render_to_response('quizzo/index.html', variables)


def quiz_page(request, quiz_id, quiz_slug):
    """
    Displays a single quiz as a form along with links
    to the previous and next quizzes.
    """
    quiz = get_object_or_404(Quiz, id=quiz_id, slug=quiz_slug)

    pre, next = _get_next_and_previous(quiz)

    variables = RequestContext(request, {
        'quiz': quiz,
        'previous': pre,
        'next': next
    })
    return render_to_response('quizzo/quiz_page.html', variables)


def quiz_results(request, quiz_id, quiz_slug):
    """
    This is where the magic happens.
    Checks for POST data, then grade the quiz.
    If no post data, redirect to quiz page.
    """
    if request.method == 'POST':
        score = 0
        quiz = Quiz.objects.get(id=quiz_id, slug=quiz_slug)
        pre, next = _get_next_and_previous(quiz)
        questions = quiz.questions.all()
        results = []
        for question in questions:
            possible_answers = question.answer_set.all()
            user_answer_id = request.POST['question_%s' % question.id]
            user_answer = get_object_or_404(Answer, id=user_answer_id)
            if user_answer in possible_answers:
                user_answer.guesses += 1
                user_answer.save()
                correct_answer, num_guesses = _get_correct_answer(question)
                if correct_answer == user_answer:
                    score += 1
                    correct = True
                else:
                    correct = False
                results.append([question, correct, num_guesses, correct_answer, user_answer])
            else:
                return HttpResponseRedirect('/webapps/quiz/%s/%s' % (quiz_id, quiz_slug))
        variables = RequestContext(request, {
            'quiz': quiz,
            'results': results,
            'score': score,
            'previous': pre,
            'next': next
            })
        return render_to_response('quizzo/results_page.html', variables)
    else:
        return HttpResponseRedirect('/webapps/quiz/%s/%s' % (quiz_id, quiz_slug))


def search_page(request):
    """
        Support both AJAX and standard requests.
        If AJAX, this view returns the quiz_list.
        Else, it returns the search page.
    """
    form = SearchForm()
    show_results = False
    pagination = False

    variables = RequestContext(request, {
        'form': form,
        'show_results': show_results,
        'pagination': pagination
    })

    if 'query' in request.GET:
        show_results = True
        pagination = False
        query = request.GET['query'].strip()

        if query:
            form = SearchForm({'query': query})
            quizzes = Quiz.objects.filter(
                Q(headline__icontains=query) | Q(blurb__icontains=query)
                ).order_by('-pub_date')
            variables = RequestContext(request, {
                'form': form,
                'quizzes': quizzes,
                'show_results': show_results,
                'pagination': pagination
            })

    if 'ajax' in request.GET:
        return render_to_response('quizzo/quiz_list.html', variables)
    else:
        return render_to_response('quizzo/search.html', variables)
