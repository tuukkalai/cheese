import json
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Question, Choice


def index(request):
	if request.user.is_authenticated:
		latest_question_list = Question.objects.order_by('-pub_date')[:5]
		return render(request, 'polls/index.html', {'latest_question_list': latest_question_list, 'user': request.user})
	return HttpResponseRedirect('login')

def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/results.html', {'question': question})

@login_required
def create(request):
	return render(request, 'polls/create_question.html')

@csrf_exempt
def vote(request, question_id):
	"""With get_object_or_404 an 404 error would be shown if Question with given id is not found."""
	
	# question = get_object_or_404(Question, pk=question_id)
	question = Question.objects.get(pk=question_id)

	try:
		"""
		Method POST should be used when user inputs interacts with database.
		
		"Whenever you create a form that alters data server-side, use method="post".
		This tip isn’t specific to Django; it’s good web development practice in general."
		(https://docs.djangoproject.com/en/4.0/intro/tutorial04/#write-a-minimal-form)
		
		Following variable selected_choice is gained with choice parameter in the request.
		-> Vote could be added with just an URL (e.g. /2/results/vote/?choice=6).
		Doesn't matter which question id is set in the URL.
		"""

		# selected_choice = question.choice_set.get(pk=request.POST['choice'])
		selected_choice = Choice.objects.get(pk=request.GET['choice'])

	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes = F('votes') + 1
		selected_choice.save()
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

@csrf_exempt
def question(request, question_id=-1):
	if request.method == 'POST':
		question = request.POST.get('questionField')

		new_question = Question.objects.create(
			question_text=question,
			pub_date=timezone.now()
		)
		# query = "INSERT INTO polls_question (question_text, pub_date) " \
			# "VALUES ('" + question + "', '" + str(timezone.now()) + "');"
		# new_question = Question.objects.raw(query)

		return redirect('/')

	if request.method == 'GET':
		"""
		SQL Injection.
		Adding query directly with raw-method and insecure way of adding user input in query.

		Question ID is extracted from URL and injected directly to query.
		Following URL prints admin users password hash on the screen:
		/question/2%20AND%201%3D2%20UNION%20SELECT%20username%2C%20password%2C%20id%20FROM%20auth_user%20WHERE%20is_superuser%3D1
		"""
		questions = Question.objects.raw("SELECT id, question_text, pub_date FROM polls_question;")
		if question_id != -1:
			query = f"SELECT * FROM polls_question WHERE id={question_id};"
			questions = Question.objects.raw(query)

		return render(request, 'polls/index.html', {'latest_question_list': questions})
	
	return HttpResponse('Nothing was found/added')
