from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from .models import Question, Choice


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    # Django provides the context variable "question" automatically since we are using the Question model
    # and it knows which Question to use since the pk is provided in the urlconf (djb - 1 Sep 18).
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # request.Post is a dictionary-like object that lets you access submitted data by key name.
        # In this case, request.POST['choice'] returns the ID of the selected choice, as a string.
        # request.POST values are always strings.
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    selected_choice.votes += 1
    selected_choice.save()
    # Always return an HttpResponseRedirect after successfully dealing with POST data. This prevents data from
    # being posted twice if a user hits the Back button.
    # The reverse function has access to the URL map that Django uses to find a view function for incoming URLs.
    # In this case, you pass in a view function, and the arguments it will get, and it finds the URL that maps to it.
    # Then the HttpResponseRedirect function creates a response that directs the browser to visit that URL.
    return HttpResponseRedirect(reverse('poll:results', args=(question.id,)))


'''
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # The context is a dictionary mapping template variable names to Python objects.
    context = {'latest_question_list': latest_question_list}
    return render(request, 'Poll/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'Poll/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'Poll/results.html', {'question': question})
'''
