from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from matplotlib.style import context
import matplotlib.pyplot as plt
from io import StringIO
import numpy as np
from .models import Question, Choice, Vote

# Create your views here.
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip=x_forwarded_for.split(',')[0]
    else:
        ip=request.META.get('REMOTE_ADDR')
    return ip

def get_graph(question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = [choice for choice in Choice.objects.all() if choice.question == question]
    labels = [choice.choice_text for choice in choices]
    votes = [choice.votes for choice in choices]

    fig = plt.figure()
    plt.bar(range(len(choices)), votes, tick_label = labels, width = 0.2, color = "purple")

    plt.xlabel("Meals")
    plt.ylabel("Votes")
    plt.title(question.question_text)

    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)

    data = imgdata.getvalue()
    return data

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    choices = question.choice_set.all() #for rook, choice_set is automatically created by Django, it refers to all choices associated to a particular question
    return render(request, 'polls/detail.html', {'question': question, 'choices': choices})

def index(request):
    data = [get_graph(1), get_graph(2), get_graph(3)]
    questions = Question.objects.all()  # Get all questions
    return render(request, 'polls/index.html', {'questions': questions, 'bf_graph': data[0], "ln_graph": data[1], "dn_graph": data[2]})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # Get the selected choice
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # If no choice is selected or an invalid choice is selected
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # Check if the user has already voted (if required)
        if Vote.objects.filter(ip_address=request.META.get('REMOTE_ADDR'), question=question).exists():
            return HttpResponse("You have already voted for this question.", status=400)

        # Create a new vote for the selected choice
        selected_choice.votes += 1
        selected_choice.save()

        # Save the vote in the Vote model
        Vote.objects.create(choice=selected_choice, ip_address=request.META.get('REMOTE_ADDR'))

        # Redirect to results after voting
        return redirect('polls:results', question_id=question.id)
    

